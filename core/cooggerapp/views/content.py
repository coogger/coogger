#django
from django.contrib.auth.models import User
from django.views.decorators.clickjacking import xframe_options_exempt
from django.utils.decorators import method_decorator
from django.views import View
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.views.generic.base import TemplateView
from django.contrib import messages
from django.template.loader import render_to_string
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import F
from django.utils import timezone

#core.cooggerapp models
from ..models import Content, UTopic, Commit, Category, Topic
from ..models.utils import ready_tags, dor, get_first_image, is_comment

#core.cooggerapp.views 
from ..views.generic.detail import DetailPostView

#forms
from ..forms import ContentReplyForm, ContentUpdateForm, ContentCreateForm

class Detail(DetailPostView, View):
    model = Content
    model_name = "content"
    template_name = "content/detail/detail.html"
    form_class = ContentReplyForm
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

    def get_object(self, username, permlink):
        return get_object_or_404(Content, user__username=username, permlink=permlink)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        queryset = context.get("queryset")
        context["current_user"] = queryset.user
        context["current_page_permlink"] = queryset.permlink
        context["nameoflist"] = queryset.utopic
        return context


@method_decorator(xframe_options_exempt, name="dispatch")
class Embed(Detail):
    template_name = "content/detail/embed.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["embed"] = True
        return context


class TreeDetail(TemplateView):
    template_name = "content/detail/tree.html"
    #TODO
    #url '@username/topic_permlink/tree/hash/'
    #or url can be
    #url '/tree/hash/' because hash is unique

    #TODO show all replies acording to commit date, 
    #use Detail class but all data must be acording to commit date

    def get_context_data(self, username, topic_permlink, hash, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context["current_user"] = User.objects.get(username=username)
        context["queryset"] = Commit.objects.get(hash=hash)
        return context


def redirect_utopic(request, utopic_permlink):
    messages.warning(request, f"you need to create the {utopic_permlink} topic first.")
    return redirect(reverse("create-utopic")+f"?name={utopic_permlink}")


class Create(LoginRequiredMixin, View):
    #TODO use createview class as inherit
    template_name = "content/post/create.html"
    form_class = ContentCreateForm
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
            form.tags = ready_tags(form.tags) #make validation
            form.save()
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
    #TODO use updateview class as inherit
    template_name = "content/post/update.html"
    form_class = ContentUpdateForm
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
                if is_comment(queryset[0]):
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
            queryset = get_object_or_404(self.model, user=request.user, permlink=permlink)
            if is_comment(queryset):
                form = self.reply_form_class(data=request.POST)
            else:
                form = self.form_class(data=request.POST)
            if form.is_valid():
                form = form.save(commit=False)
                form.user = request.user
                if is_comment(queryset):
                        "if its a comment"
                        queryset.body = form.body
                        queryset.image_address = get_first_image(form.body)
                        queryset.last_update = timezone.now()
                        queryset.save()
                else:
                    get_utopic_permlink = request.GET.get("utopic_permlink", None)
                    if get_utopic_permlink is None:
                        utopic = queryset.utopic
                    else:
                        utopic = UTopic.objects.filter( #new utopic
                            user=queryset.user, 
                            permlink=get_utopic_permlink
                        )
                        utopic.update( #new utopic update
                            how_many=(F("how_many") + 1),
                            total_dor=(F("total_dor") + dor(form.body)),
                            total_view=(F("total_view") + queryset.views)
                        )
                        UTopic.objects.filter( #old utopic update
                            user=queryset.user,
                            permlink=queryset.utopic.permlink
                        ).update(
                            how_many=(F("how_many") - 1),
                            total_dor=(F("total_dor") - dor(queryset.body)),
                            total_view=(F("total_view") - queryset.views)
                        )
                        utopic = utopic[0]
                        Commit.objects.filter( #old utopic update to new utopic commit
                            utopic=queryset.utopic,
                            content=queryset
                        ).update(
                            utopic=utopic
                        )
                    if form.body != queryset.body:
                        Commit(
                            user=queryset.user,
                            utopic=utopic,
                            content=queryset,
                            body=form.body,
                            msg=request.POST.get("msg")
                        ).save()
                    queryset.image_address = get_first_image(form.body)
                    queryset.category = form.category
                    queryset.language = form.language
                    queryset.tags = ready_tags(form.tags)
                    queryset.body = form.body
                    queryset.title = form.title
                    queryset.last_update = timezone.now()
                    update_fields = []
                    if queryset.status != form.status:
                        queryset.status = form.status
                        update_fields=["status"]
                    queryset.utopic = utopic
                    queryset.save(update_fields=update_fields) # to content signals
                return redirect(
                    reverse(
                        "content-detail", 
                        kwargs=dict(
                            username=str(queryset.user), 
                            permlink=queryset.permlink
                            )
                        )
                    )
            context = dict(
                form=form,
                username=username,
                permlink=permlink
            )
            return render(request, self.template_name, context)
