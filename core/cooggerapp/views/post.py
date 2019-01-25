# django
from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import Http404
from django.template.loader import render_to_string

# class base
from django.views import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

# models
from core.cooggerapp.models import Content, CategoryofDapp
from core.steemconnect_auth.models import Dapp

# form
from core.cooggerapp.forms import ContentForm

# choices
from core.cooggerapp.choices import make_choices

# steem
from steem.post import Post


class Create(View):
    template_name = "post/create.html"
    initial = {}
    category_name = None
    dapp_id = 1

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        for key, value in request.GET.items():
            if key == "dapp":
                self.dapp_id = value
            elif key == "category":
                self.category_name = value
            else:
                self.initial[key] = value
        category_content = render_to_string("post/editor-note.html")
        if self.category_name is not None:
            dapp_model = request.dapp_model
            if dapp_model.name == "coogger":
                category_content = CategoryofDapp.objects.get(
                    name=self.category_name
                ).editor_template
            else:
                category_content = CategoryofDapp.objects.get(
                    dapp=dapp_model, name=self.category_name
                ).editor_template
        if self.dapp_id is not None:
            dapp_model = Dapp.objects.filter(id=self.dapp_id)[0]
            request.dapp_model = dapp_model
            category_filter = CategoryofDapp.objects.filter(dapp=dapp_model)
            request.categories = make_choices([category.name for category in category_filter])
        self.initial["content"] = category_content
        self.initial["category"] = self.category_name
        self.initial["dapp"] = request.dapp_model
        form = ContentForm(request=request, initial=self.initial)
        return render(request, self.template_name, {"form": form})

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        dapp_id = request.GET.get("dapp", None)
        if dapp_id is not None:
            dapp_model = Dapp.objects.filter(id=dapp_id)[0]
            request.dapp_model = dapp_model
            category_filter = CategoryofDapp.objects.filter(dapp=dapp_model)
            request.categories = make_choices([category.name for category in category_filter])
        form = ContentForm(data=request.POST, request=request)
        if form.is_valid():
            form = form.save(commit=False)
            form.user = request.user
            save = form.content_save(request)  # save with steemconnect and get ms
            if save.status_code != 200:  # if any error show the error
                messages.error(request, save.text)
                return render(request, self.template_name, dict(form=form))
            return redirect("/"+form.get_absolute_url)
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
                    category_filter = CategoryofDapp.objects.filter(dapp=dapp_model)
                    request.categories = make_choices([category.name for category in category_filter])
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
                    category_filter = CategoryofDapp.objects.filter(dapp=dapp_model)
                    request.categories = make_choices([category.name for category in category_filter])
                else:
                    queryset = queryset.filter(dapp=dapp_model)
                    if not queryset.exists():
                        raise Http404
                form = ContentForm(data=request.POST, request=request)
                maybe_error_form = form
                if form.is_valid():
                    form = form.save(commit=False)
                    save = form.content_update(old=queryset, new=form)
                    if save.status_code != 200:
                        messages.error(request, save.text)
                        warning_ms = """unexpected error, check your content please or contact us on discord;
                        <a gnrl='c-primary' href='https://discord.gg/avmdZJa'>https://discord.gg/avmdZJa</a>"""
                        messages.error(request, warning_ms)
                        return render(request, self.template_name, dict(
                            form=maybe_error_form,
                            username=username,
                            permlink=permlink)
                        )
                    return redirect("/"+queryset[0].get_absolute_url)
                else:
                    messages.error(request, form.errors)
                    warning_ms = """unexpected error, check your content please or contact us on discord;
                    <a gnrl='c-primary' href='https://discord.gg/avmdZJa'>https://discord.gg/avmdZJa</a>"""
                    return render(request, self.template_name, dict(
                        form=form,
                        username=username,
                        permlink=permlink)
                    )
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
