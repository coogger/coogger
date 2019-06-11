# django
from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import Http404
from django.template.loader import render_to_string
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.db.models import F
from django.utils import timezone

# models
from ..models import Content, Category, UTopic, Topic, Commit
from ..models.utils import ready_tags, dor, content_definition

# form
from ..forms import ContentForm, ReplyForm


def redirect_utopic(request, utopic_permlink):
    messages.warning(request, f"you need to create the {utopic_permlink} topic first.")
    return redirect(reverse("create-utopic")+f"?name={utopic_permlink}")


class Create(LoginRequiredMixin, View):
    template_name = "post/create.html"
    form_class = ContentForm
    initial_template = "post/editor-note.html"

    def get(self, request, utopic_permlink, *args, **kwargs):
        initial, category = dict(), None
        if not UTopic.objects.filter(user=request.user, permlink=utopic_permlink).exists():
            return redirect_utopic(request, utopic_permlink)
        for key, value in request.GET.items():
            if key == "category":
                category = Category.objects.get(name=value)
                category_template = category.template
                initial.__setitem__("category", category)
            else:
                initial.__setitem__(key, value)
        if category is None:
            category_template = render_to_string(self.initial_template)
        initial.__setitem__("body", category_template)
        initial.__setitem__("msg", "Initial commit")
        context = dict(
            form=self.form_class(initial=initial)
        )
        return render(request, self.template_name, context)

    def post(self, request, utopic_permlink, *args, **kwargs):
        form = self.form_class(data=request.POST)
        if form.is_valid():
            form = form.save(commit=False)
            user_topic = UTopic.objects.filter(user=request.user, permlink=utopic_permlink)
            form.user = request.user
            form.utopic = user_topic[0]
            form.tags = ready_tags(form.tags) # make validation
            form.save()
            self.form_class.send_mail(form)
            user_topic.update(how_many=F("how_many") + 1)
            topic_model = Topic.objects.filter(permlink=utopic_permlink)
            topic_model.update(how_many=F("how_many") + 1) # increae how_many in Topic model
            user_topic.update(total_dor=F("total_dor") + dor(form.body)) # increase total dor in utopic
            get_msg = request.POST.get("msg", None)
            if get_msg == "Initial commit":
                get_msg = f"{form.title} Published."
            Commit(
                user=form.user,
                utopic=form.utopic,
                content=form,
                body=form.body,
                msg=get_msg,
            ).save()
            return redirect(
                reverse(
                    "detail", 
                    kwargs=dict(
                        username=str(form.user), 
                        permlink=form.permlink
                    )
                )
            )
        return render(request, self.template_name, dict(form=form))


class Update(LoginRequiredMixin, View):
    template_name = "post/update.html"
    form_class = ContentForm
    reply_form_class = ReplyForm
    model = Content

    def get(self, request, username, permlink, *args, **kwargs):
        if request.user.username == username:
            utopic_permlink = request.GET.get("utopic_permlink", None)
            if utopic_permlink is not None and not UTopic.objects.filter(
                user=request.user, permlink=utopic_permlink).exists():
                return redirect_utopic(request, utopic_permlink)
            queryset = self.model.objects.filter(user=request.user, permlink=permlink)
            if queryset.exists():
                if queryset[0].reply is not None:
                    form_set = self.reply_form_class(instance=queryset[0])
                else:
                    form_set = self.form_class(
                        instance=queryset[0], 
                        initial=dict(
                            msg=f"Update {queryset[0].title.lower()}"
                        )
                    )
                context = dict(
                    username=username,
                    permlink=permlink,
                    form=form_set,
                )
                return render(request, self.template_name, context)

    def post(self, request, username, permlink, *args, **kwargs):
        if request.user.username == username:
            queryset = self.model.objects.filter(user=request.user, permlink=permlink)
            if queryset.exists():
                if queryset[0].reply is not None:
                    form = self.reply_form_class(data=request.POST)
                else:
                    form = self.form_class(data=request.POST)
                if form.is_valid():
                    form = form.save(commit=False)
                    form.user = request.user
                    if queryset[0].reply is not None:
                        "if its a comment"
                        queryset.update(
                            title=form.title,
                            body=form.body,
                            definition=content_definition(form.body),
                            last_update=timezone.now(),
                        )
                    else:
                        get_utopic_permlink = request.GET.get("utopic_permlink", None)
                        if get_utopic_permlink is None:
                            utopic = queryset[0].utopic
                        else:
                            utopic = UTopic.objects.get(
                                user=queryset[0].user, 
                                permlink=get_utopic_permlink
                            )
                        if form.body != queryset[0].body:
                            Commit(
                                user=queryset[0].user,
                                utopic=utopic,
                                content=queryset[0],
                                body=form.body,
                                msg=request.POST.get("msg")
                            ).save()
                        queryset.update(
                            definition=content_definition(form.body),
                            category=form.category,
                            language=form.language,
                            tags=ready_tags(form.tags),
                            body=form.body,
                            title=form.title,
                            last_update=timezone.now(),
                            utopic=utopic,
                        )
                    return redirect(
                        reverse(
                            "detail", 
                            kwargs=dict(
                                username=str(queryset[0].user), 
                                permlink=queryset[0].permlink
                                )
                            )
                        )
                context = dict(
                    form=form,
                    username=username,
                    permlink=permlink
                )
                return render(request, self.template_name, context)
