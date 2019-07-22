#django
from django.contrib.auth.models import User
from django.views.decorators.clickjacking import xframe_options_exempt
from django.utils.decorators import method_decorator
from django.views import View
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.db.utils import IntegrityError
from django.contrib.contenttypes.models import ContentType
from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView
from django.contrib import messages
from django.template.loader import render_to_string
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import F
from django.utils import timezone

#core.cooggerapp models
from ..models import Content, UTopic, Commit, Category, Topic
from ..models.utils import ready_tags, dor, get_first_image

#django libs
from django_page_views.models import DjangoViews

#forms
from ..forms import ContentReplyForm, ContentForm

#utils
from ..models.utils import send_mail

#python
import json

class Detail(View):
    model = Content
    template_name = "content/detail/detail.html"
    reply_form_class = ContentReplyForm
    #fields that remain the same when commented.
    same_fields = [
        "title",
        "utopic", 
        "language", 
        "category", 
        "tags",
        "status", 
    ]
    #json respon fields after commented
    response_field = [
        "id",
        "user.username",
        "utopic.permlink",
        "parent_permlink",
        "parent_user",
        "created",
        "reply_count",
        "status",
        "reply_id",
        "body",
        "title",
        "permlink",
        "user.githubauthuser.avatar_url",
        "get_absolute_url",
    ]

    def save_view(self, request, id):
        get_view, created = DjangoViews.objects.get_or_create(
            content_type=ContentType.objects.get(
                app_label="cooggerapp", 
                model="content"
            ), 
            object_id=id
        )
        try:
            get_view.ips.add(request.ip_model)
        except IntegrityError:
            pass

    def get_object(self, username, permlink):
        return get_object_or_404(Content, user__username=username, permlink=permlink)

    def get(self, request, username, permlink):
        content = self.get_object(username, permlink)
        self.save_view(request, content.id)
        context = dict(
            current_user=content.user,
            urloftopic=permlink,
            nameoflist=content.utopic,
            queryset=content,
            reply_form=self.reply_form_class,
        )
        return render(request, self.template_name, context)

    @method_decorator(login_required)
    def post(self, request, username, permlink, *args, **kwargs):
        "This function works when making a new comment/reply"
        parent_content = self.get_object(username, permlink)
        reply_form = self.reply_form_class(request.POST)
        if reply_form.is_valid():
            reply_form = reply_form.save(commit=False)
            reply_form.user = request.user
            reply_form.reply = parent_content
            for field in self.same_fields:
                setattr(reply_form, field, getattr(parent_content, field))
            reply_form.save()
            email_list = list()
            for obj in parent_content.get_all_reply_obj():
                email = obj[0].user.email
                if (obj[0].user != request.user) and (email) and (email not in email_list):
                    email_list.append(email)
            send_mail(
                subject=f"{ request.user } left a comment on your post | Coogger", 
                template_name="email/reply.html", 
                context=dict(
                    user=request.user,
                    get_absolute_url=reply_form.get_absolute_url,
                ),
                to=email_list
            )
            context = dict()
            for field in self.response_field:
                s = field.split(".")
                if len(s) == 1:
                    context[field] = str(getattr(reply_form, field))
                else:
                    obj = reply_form
                    for f in s:
                        obj = getattr(obj, f)
                    value = str(obj)
                    context[s[-1]] = value
            return HttpResponse(json.dumps(context))


@method_decorator(xframe_options_exempt, name="dispatch")
class Embed(Detail):
    template_name = "content-detail/embed.html"


class TreeDetail(TemplateView):
    template_name = "content-detail/tree.html"
    # TODO
    # url '@username/topic_permlink/tree/hash/'
    # or url can be
    # # url '/tree/hash/' because hash is unique

    def get_context_data(self, username, topic_permlink, hash, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context["current_user"] = User.objects.get(username=username)
        context["queryset"] = Commit.objects.get(hash=hash)
        return context


def redirect_utopic(request, utopic_permlink):
    messages.warning(request, f"you need to create the {utopic_permlink} topic first.")
    return redirect(reverse("create-utopic")+f"?name={utopic_permlink}")


class Create(LoginRequiredMixin, View):
    template_name = "content/post/create.html"
    form_class = ContentForm
    initial_template = "content/post/editor-note.html"

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
            Topic.objects.filter(
                permlink=utopic_permlink
            ).update(
                how_many=(F("how_many") + 1)
            ) # increae how_many in Topic model
            user_topic.update(
                how_many=(F("how_many") + 1),
                total_dor=(F("total_dor") + dor(form.body))
            ) # increase total dor in utopic
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
                    "content-detail", 
                    kwargs=dict(
                        username=str(form.user), 
                        permlink=form.permlink
                    )
                )
            )
        return render(request, self.template_name, dict(form=form))


class Update(LoginRequiredMixin, View):
    template_name = "content/post/update.html"
    form_class = ContentForm
    reply_form_class = ContentReplyForm
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
        return HttpResponse(status=403)

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
                            body=form.body,
                            image_address=get_first_image(form.body),
                            last_update=timezone.now(),
                        )
                    else:
                        get_utopic_permlink = request.GET.get("utopic_permlink", None)
                        if get_utopic_permlink is None:
                            utopic = queryset[0].utopic
                        else:
                            utopic = UTopic.objects.filter( # new utopic
                                user=queryset[0].user, 
                                permlink=get_utopic_permlink
                            )
                            utopic.update( # new utopic update
                                how_many=(F("how_many") + 1),
                                total_dor=(F("total_dor") + dor(form.body)),
                                total_view=(F("total_view") + queryset[0].views)
                            )
                            UTopic.objects.filter( # old utopic update
                                user=queryset[0].user,
                                permlink=queryset[0].utopic.permlink
                            ).update(
                                how_many=(F("how_many") - 1),
                                total_dor=(F("total_dor") - dor(queryset[0].body)),
                                total_view=(F("total_view") - queryset[0].views)
                            )
                            utopic = utopic[0]
                            Commit.objects.filter( # old utopic update to new utopic commit
                                utopic=queryset[0].utopic,
                                content=queryset[0]
                            ).update(
                                utopic=utopic
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
                            image_address=get_first_image(form.body),
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
                            "content-detail", 
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
        return HttpResponse(status=403)
