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
from beem.exceptions import ContentDoesNotExistsException


class CreateUTopic(View):
    template_name = "post/utopic.html"
    form_class = UTopicForm
    model = UTopic

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        initial = dict()
        for key, value in request.GET.items():
            initial.__setitem__(key, value)
        return render(request, self.template_name, {"form": self.form_class(initial=initial)})

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


class Create(View):
    template_name = "post/create.html"
    form_class = ContentForm
    initial_template = "post/editor-note.html"

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        initial, category = dict(), None
        if request.GET.get("topic", None) is None:
            messages.warning(request, "you need to write like that /post/create/?topic={your_topic_name} or create the topic first.")
            return redirect(f"/post/utopic/")
        for key, value in request.GET.items():
            if key == "category":
                category = Category.objects.get(name=value)
                category_template = category.template
                initial.__setitem__("category", category)
            elif key == "topic":
                try:
                    utopic = UTopic.objects.filter(user=request.user, name=value)[0]
                except IndexError:
                    messages.warning(request, f"you need to create the {value} topic first.")
                    return redirect(f"/post/utopic/?name={value}")
                initial.__setitem__("topic", utopic)
            else:
                initial.__setitem__(key, value)
        if category is None:
            category_template = render_to_string(self.initial_template)
        initial.__setitem__("content", category_template)
        initial.__setitem__("msg", "Initial commit")
        context = dict(
            form=self.form_class(initial=initial)
        )
        return render(request, self.template_name, context)

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        form = self.form_class(data=request.POST)
        if form.is_valid():
            form = form.save(commit=False)
            save = form.content_save(request)  # save with steemconnect and get ms
            if save.status_code != 200:  # if any error show the error
                messages.error(request, save.text)
                return render(request, self.template_name, dict(form=ContentForm(data=request.POST)))
            return redirect(form.get_absolute_url)
        else:
            return render(request, self.template_name, dict(form=form))


class Change(View):
    template_name = "post/change.html"
    form_class = ContentForm
    model = Content

    @method_decorator(login_required)
    def get(self, request, username, permlink, *args, **kwargs):
        if request.user.username == username:
            queryset = self.model.objects.filter(user=request.user, permlink=permlink)
            if queryset.exists():
                content_id = queryset[0].id
                self.content_update(request, content_id)
                queryset = self.model.objects.filter(user=request.user, permlink=permlink)[0]
                context = dict(
                    username=username,
                    permlink=permlink,
                    form=self.form_class(instance=queryset, initial=dict(msg=f"Update {queryset.title.lower()}")),
                )
                return render(request, self.template_name, context)
        raise Http404

    @method_decorator(login_required)
    def post(self, request, username, permlink, *args, **kwargs):
        if request.user.username == username:
            queryset = self.model.objects.filter(user=request.user, permlink=permlink)
            if queryset.exists():
                content_id = queryset[0].id
                form = self.form_class(data=request.POST)
                if form.is_valid():
                    form = form.save(commit=False)
                    save = form.content_update(request=request, old=queryset, new=form)
                    if save.status_code != 200:
                        messages.error(request, save.text)
                        return render(request, self.template_name, dict(
                            form=self.form_class(data=request.POST),
                            username=username,
                            permlink=permlink)
                        )
                    return redirect(queryset[0].get_absolute_url)
                else:
                    context = dict(
                        form=form,
                        username=username,
                        permlink=permlink
                    )
                    return render(request, self.template_name, context)
        raise Http404

    def content_update(self, request, content_id): # is it necessary
        content = self.model.objects.filter(id=content_id)
        try:
            beem_comment = Comment(content[0].get_absolute_url)
        except ContentDoesNotExistsException:
            # delete this content
            pass
        else:
            content.update(body=self.get_body_from_steem(beem_comment), title=beem_comment.title)

    def get_body_from_steem(self, post):
        json_metadata = post.get("json_metadata")
        try:
            ecosystem = json_metadata.get("ecosystem")
        except (KeyError, TypeError):
            return post.body
        else:
            try:
                version = ecosystem.get("version")
            except (TypeError, KeyError):
                return post.body
            else:
                if version == "1.4.1":
                    return ecosystem.get("body")
                else:
                    return post.body
