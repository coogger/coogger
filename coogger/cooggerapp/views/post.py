# django
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.db.models import F
from django.contrib import messages as ms

# class
# from django.views.generic import ListView
from django.views import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.http import Http404

# models
from cooggerapp.models import Content, CategoryofDapp
from steemconnect_auth.models import Dapp

# views
from cooggerapp.views.tools import get_user

# form
from cooggerapp.forms import ContentForm

# choices
from cooggerapp.choices import *

# steem
from steem.post import Post


class Create(View):
    template_name = "post/create.html"

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        category_name = request.GET.get("category", None)
        dapp_id = request.GET.get("dapp", None)
        if dapp_id is None and request.dapp_model.name == "coogger":
            dapp_id = 1
        category_content = ""
        if category_name is not None:
            dapp_model = request.dapp_model
            if dapp_model.name == "coogger":
                category_content = CategoryofDapp.objects.get(
                    category_name=category_name
                ).editor_template
            else:
                category_content = CategoryofDapp.objects.get(
                    dapp=dapp_model, category_name=category_name
                ).editor_template
        if dapp_id is not None:
            dapp_model = Dapp.objects.filter(id=dapp_id)[0]
            request.dapp_model = dapp_model
            category_filter = CategoryofDapp.objects.filter(dapp=dapp_model)
            request.categories = make_choices([category.category_name for category in category_filter])
        form = ContentForm(
            request=request,
            initial={"content": category_content, "category":category_name, "dapp": request.dapp_model}
        )
        return render(request, self.template_name, {"form": form})

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        dapp_id = request.GET.get("dapp", None)
        if dapp_id is not None:
            dapp_model = Dapp.objects.filter(id=dapp_id)[0]
            request.dapp_model = dapp_model
            category_filter = CategoryofDapp.objects.filter(dapp=dapp_model)
            request.categories = make_choices([category.category_name for category in category_filter])
        form = ContentForm(data=request.POST, request=request)
        if form.is_valid():
            form = form.save(commit=False)
            form.user = request.user
            save = form.content_save(request)  # save with steemconnect and get ms
            if save.status_code != 200:  # if any error show the error
                ms.error(request, save.text)
                return render(request, self.template_name, dict(form=form))
            return HttpResponseRedirect("/"+form.get_absolute_url)
        else:
            return render(request, self.template_name, dict(form=form))


class Change(View):
    template_name = "post/change.html"

    @method_decorator(login_required)
    def get(self, request, username, permlink, *args, **kwargs):
        if request.user.username == username:
            queryset = Content.objects.filter(user=request.user, permlink=permlink)
            if queryset.exists():
                content_id = queryset[0].id
                self.content_update(request, content_id)
                queryset = Content.objects.filter(user=request.user, permlink=permlink)
                dapp_model = request.dapp_model
                if dapp_model.name == "coogger":
                    request.dapp_model = queryset[0].dapp
                    category_filter = CategoryofDapp.objects.filter(dapp=request.dapp_model)
                    request.categories = make_choices([category.category_name for category in category_filter])
                else:
                    queryset = queryset.filter(dapp=dapp_model)
                    if not queryset.exists():
                        raise Http404
                content_form = ContentForm(instance=queryset[0], request=request)
                context = dict(
                    username=username,
                    permlink=permlink,
                    form=content_form,
                )
                return render(request, self.template_name, context)
        raise Http404

    @method_decorator(login_required)
    def post(self, request, username, permlink, *args, **kwargs):
        if request.user.username == username:
            queryset = Content.objects.filter(user=request.user, permlink=permlink)
            if queryset.exists():
                content_id = queryset[0].id
                dapp_model = request.dapp_model
                if dapp_model.name == "coogger":
                    request.dapp_model = queryset[0].dapp
                    category_filter = CategoryofDapp.objects.filter(dapp=request.dapp_model)
                    request.categories = make_choices([category.category_name for category in category_filter])
                else:
                    queryset = queryset.filter(dapp=dapp_model)
                    if not queryset.exists():
                        raise Http404
                form = ContentForm(data=request.POST, request=request)
                maybe_error_form = form
                if form.is_valid():
                    form = form.save(commit=False)
                    save = form.content_update(queryset, form)
                    if save.status_code != 200:
                        ms.error(request, save.text)
                        warning_ms = """unexpected error, check your content please or contact us on discord;
                        <a gnrl='c-primary' href='https://discord.gg/avmdZJa'>https://discord.gg/avmdZJa</a>"""
                        ms.error(request, warning_ms)
                        return render(request, self.template_name, dict(
                            form=maybe_error_form,
                            username=username,
                            permlink=permlink)
                        )
                    return HttpResponseRedirect("/"+queryset[0].get_absolute_url)
        raise Http404

    def content_update(self, request, content_id):
        ct = Content.objects.filter(user=request.user, id=content_id)
        post = Post(post=ct[0].get_absolute_url)
        ct.update(content=self.get_body_from_steem(post), title=post.title)

    def get_body_from_steem(self, post):
        json_metadata = post["json_metadata"]
        try:
            ecosystem = json_metadata["ecosystem"]
        except (KeyError, TypeError):
            return post.body
        try:
            version = ecosystem["version"]
        except (TypeError, KeyError):
            return post.body
        if version == "1.4.1":
            return ecosystem["body"]
        else:
            return post.body
