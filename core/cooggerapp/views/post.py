# django
from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import Http404
from django.template.loader import render_to_string
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View

# models
from core.cooggerapp.models import Content, Category, UTopic, Topic

# form
from core.cooggerapp.forms import ContentForm, UTopicForm

# choices
from core.cooggerapp.choices import make_choices


class CreateUTopic(LoginRequiredMixin, View):
    template_name = "post/utopic.html"
    form_class = UTopicForm
    model = UTopic

    def get(self, request, *args, **kwargs):
        initial = dict()
        for key, value in request.GET.items():
            initial.__setitem__(key, value)
        return render(request, self.template_name, {"form": self.form_class(initial=initial)})

    def post(self, request, *args, **kwargs):
        form = self.form_class(data=request.POST)
        if form.is_valid():
            form = form.save(commit=False)
            form.user = request.user
            if not self.model.objects.filter(user=request.user, name=form.name).exists():
                save = form.save()
                if not Topic.objects.filter(name=form.name).exists():
                    Topic(name=form.name).save()
                return redirect(reverse("utopic", kwargs={"topic": form.name, "username": form.user}))
            else:
                messages.warning(request, f"{form.name} is already taken by yours" )
                return render(request, self.template_name, dict(form=self.form_class(data=request.POST)))
        else:
            return render(request, self.template_name, dict(form=form))


class UpdateUTopic(CreateUTopic):
    template_name = "post/updateutopic.html"

    def get(self, request, name, *args, **kwargs):
        try:
            instance = self.model.objects.filter(user=request.user, name=name)[0]
        except IndexError:
            messages.warning(request, f"you need to create the {value} topic first.")
            return redirect(reverse("create-utopic")+"?name={value}")
        context = dict(
            form=self.form_class(instance=instance),
            name=name
        )
        return render(request, self.template_name, context)

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


class Create(LoginRequiredMixin, View):
    template_name = "post/create.html"
    form_class = ContentForm
    initial_template = "post/editor-note.html"

    def get(self, request, *args, **kwargs):
        initial, category = dict(), None
        topic_name = request.GET.get("topic", None)
        if topic_name is None:
            messages.warning(request, "you need to write like that /post/create/?topic={your_topic_name} or create the topic first.")
            return redirect(reverse("create-utopic"))
        else:
            if not Topic.objects.filter(name=topic_name).exists():
                messages.warning(request, f"you need to create the {topic_name} topic first.")
                return redirect(reverse("create-utopic")+f"?name={topic_name}")
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
                    return redirect(reverse("create-utopic")+"?name={value}")
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

    def post(self, request, *args, **kwargs):
        form = self.form_class(data=request.POST)
        if form.is_valid():
            form = form.save(commit=False)
            save = form.content_save(request)  # save with steemconnect and get ms
            if save.status_code != 200:  # if any error show the error
                messages.error(request, save.text)
                return render(request, self.template_name, dict(form=ContentForm(data=request.POST)))
            return redirect(reverse("detail", kwargs=dict(username=form.username, permlink=form.permlink)))
        else:
            return render(request, self.template_name, dict(form=form))


class Change(LoginRequiredMixin, View):
    template_name = "post/change.html"
    form_class = ContentForm
    model = Content

    def get(self, request, username, permlink, *args, **kwargs):
        if request.user.username == username:
            topic_name = request.GET.get("topic", None)
            if topic_name is not None and not Topic.objects.filter(name=topic_name).exists():
                messages.warning(request, f"you need to create the {topic_name} topic first.")
                return redirect(reverse("create-utopic")+f"?name={topic_name}")
            queryset = self.model.objects.filter(user=request.user, permlink=permlink)
            if queryset.exists():
                content_id = queryset[0].id
                queryset = self.model.objects.filter(user=request.user, permlink=permlink)[0]
                context = dict(
                    username=username,
                    permlink=permlink,
                    form=self.form_class(instance=queryset, initial=dict(msg=f"Update {queryset.title.lower()}")),
                )
                return render(request, self.template_name, context)
        raise Http404

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
                    return redirect(reverse("detail", kwargs=dict(username=queryset[0].username, permlink=queryset[0].permlink)))
                else:
                    context = dict(
                        form=form,
                        username=username,
                        permlink=permlink
                    )
                    return render(request, self.template_name, context)
        raise Http404
