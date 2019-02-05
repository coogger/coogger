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

# form
from core.cooggerapp.forms import ContentForm

# choices
from core.cooggerapp.choices import make_choices

# beem
from beem.comment import Comment


class Create(View):
    template_name = "post/create.html"
    initial = {}
    category_name = None

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        for key, value in request.GET.items():
            if key == "category":
                self.category_name = value
            else:
                self.initial[key] = value
        category_content = render_to_string("post/editor-note.html")
        if self.category_name is not None:
            category_content = CategoryofDapp.objects.get(
                name=self.category_name
            ).editor_template
        self.initial["content"] = category_content
        self.initial["category"] = self.category_name
        form = ContentForm(request=request, initial=self.initial)
        return render(request, self.template_name, {"form": form})

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        form = ContentForm(data=request.POST, request=request)
        if form.is_valid():
            form = form.save(commit=False)
            form.user = request.user
            save = form.content_save(request)  # save with steemconnect and get ms
            if save.status_code != 200:  # if any error show the error
                messages.error(request, save.text)
                return render(request, self.template_name, dict(form=form))
            return redirect(form.get_absolute_url)
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
                    return redirect(queryset[0].get_absolute_url)
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
        beem_comment = Comment(ct[0].get_absolute_url)
        ct.update(content=self.get_body_from_steem(beem_comment), title=beem_comment.title)

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
