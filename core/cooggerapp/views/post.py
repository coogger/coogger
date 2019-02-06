# django
from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import Http404
from django.template.loader import render_to_string
# from django.contrib.auth import authenticate

# class base
from django.views import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

# models
from core.cooggerapp.models import Content, Category, UTopic

# form
from core.cooggerapp.forms import ContentForm, UTopicForm

# choices
from core.cooggerapp.choices import make_choices

# beem
from beem.comment import Comment


class CreateUTopic(View):
    template_name = "post/utopic.html"
    form_class = UTopicForm
    model = UTopic

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {"form": self.form_class()})

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        form = self.form_class(data=request.POST)
        if form.is_valid():
            form = form.save(commit=False)
            form.user = request.user
            if not self.model.objects.filter(user=request.user, name=form.name).exists():
                save = form.save()
                return redirect(f"/{form.name}/@{form.user}")
            else:
                messages.warning(request, f"{form.name} is already taken by yours")
                return render(request, self.template_name, dict(form=self.form_class(data=request.POST)))
        else:
            return render(request, self.template_name, dict(form=form))


class UpdateUTopic(CreateUTopic):
    template_name = "post/updateutopic.html"

    @method_decorator(login_required)
    def get(self, request, name, *args, **kwargs):
        instance = self.model.objects.filter(user=request.user, name=name)[0]
        context = dict(
            form=self.form_class(instance=instance),
            name=name
        )
        return render(request, self.template_name, context)

    @method_decorator(login_required)
    def post(self, request, name, *args, **kwargs):
        form = self.form_class(data=request.POST)
        context = dict(
            form=self.form_class(data=request.POST),
            name=name,
        )
        if form.is_valid():
            form = form.save(commit=False)
            self.model.objects.filter(user=request.user, name=name).update(
                name=form.name,
                image_address=form.image_address,
                definition=form.definition,
                tags=form.tags,
                address=form.address,
            )
            return render(request, self.template_name, context)
        else:
            return render(request, self.template_name, context)


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
            category_content = Category.objects.get(
                name=self.category_name
            ).template
        self.initial["content"] = category_content
        self.initial["category"] = self.category_name
        form = ContentForm(initial=self.initial)
        return render(request, self.template_name, {"form": form})

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        form = ContentForm(data=request.POST)
        if form.is_valid():
            form = form.save(commit=False)
            form.user = request.user
            save = form.content_save(request)  # save with steemconnect and get ms
            if save.status_code != 200:  # if any error show the error
                messages.error(request, save.text)
                return render(request, self.template_name, dict(form=ContentForm(data=request.POST)))
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
                content_form = ContentForm(instance=queryset[0])
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
                form = ContentForm(data=request.POST)
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
        ct.update(body=self.get_body_from_steem(beem_comment), title=beem_comment.title)

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
