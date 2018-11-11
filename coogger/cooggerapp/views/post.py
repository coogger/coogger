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

# models
from cooggerapp.models import Content, CategoryofDapp
from steemconnect_auth.models import Dapp

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
                return self.create_error(request, form)
            return HttpResponseRedirect("/"+form.get_absolute_url())
        else:
            return self.create_error(request, form)

    def create_error(self, request, form):
        return render(request, self.template_name, {"form": form})


class Change(View):
    template_name = "post/change.html"

    @method_decorator(login_required)
    def get(self, request, content_id, *args, **kwargs):
        dapp_model = request.dapp_model
        if dapp_model.name == "coogger":
            queryset = Content.objects.filter(user=request.user, id=content_id)
            request.dapp_model = queryset[0].dapp
            category_filter = CategoryofDapp.objects.filter(dapp=request.dapp_model)
            request.categories = make_choices([category.category_name for category in category_filter])
        else:
            queryset = Content.objects.filter(dapp=dapp_model, user=request.user, id=content_id)
        if queryset.exists():
            self.content_update(request, content_id)
            content_form = ContentForm(instance=queryset[0], request=request)
            context = dict(
                content_id=content_id,
                form=content_form,
            )
            return render(request, self.template_name, context)

    @method_decorator(login_required)
    def post(self, request, content_id, *args, **kwargs):
        dapp_model = request.dapp_model
        if dapp_model.name == "coogger":
            queryset = Content.objects.filter(user=request.user, id=content_id)
            request.dapp_model = queryset[0].dapp
            category_filter = CategoryofDapp.objects.filter(dapp=request.dapp_model)
            request.categories = make_choices([category.category_name for category in category_filter])
        else:
            queryset = Content.objects.filter(dapp=dapp_model, user=request.user, id=content_id)
        if queryset.exists():
            form = ContentForm(data=request.POST, request=request)
            maybe_error_form = form
            if form.is_valid():
                form = form.save(commit=False)
                queryset = Content.objects.filter(user=request.user, id=content_id)
                save = form.content_update(queryset, form)  # save with sc2py and get ms
                if save.status_code != 200:
                    ms.error(request, save.text)
                    return self.create_error(request, maybe_error_form)
                return HttpResponseRedirect("/"+queryset[0].get_absolute_url())

    @staticmethod
    def content_update(request, content_id):
        ct = Content.objects.filter(user=request.user, id=content_id)
        steem = Post(post=ct[0].get_absolute_url())
        ct.update(content=steem.body, title=steem.title)

    def create_error(self, request, form):
        warning_ms = """unexpected error, check your content please or contact us on discord;
        <a gnrl='c-primary' href='https://discord.gg/avmdZJa'>https://discord.gg/avmdZJa</a>"""
        ms.error(request, warning_ms)
        return render(request, self.template_name, {"form": form})
