# django
from django.contrib.auth.models import User
from django.views.decorators.clickjacking import xframe_options_exempt
from django.utils.decorators import method_decorator
from django.http import Http404
from django.views import View
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.db.utils import IntegrityError
from django.contrib.contenttypes.models import ContentType
from django.views.generic.base import TemplateView

# core.cooggerapp models
from ..models import Content, UTopic, Commit
from django_page_views.models import DjangoViews

# forms
from ..forms import NewContentReplyForm

# utils
from ..models.utils import send_mail

# python
import json


class Detail(View):
    template_name = "content-detail/detail.html"
    form_class = NewContentReplyForm

    def save_view(self, request, id):
        dj_query, created = DjangoViews.objects.get_or_create(
            content_type=ContentType.objects.get(
                app_label="cooggerapp", 
                model="content"
            ), 
            object_id=id
        )
        try:
            dj_query.ips.add(request.ip_model)
        except IntegrityError:
            pass

    def get(self, request, username, permlink):
        user = User.objects.get(username=username)
        content_obj = Content.objects.filter(user=user, permlink=permlink)
        content = content_obj[0]
        if not content_obj.exists():
            raise Http404
        self.save_view(request, content.id)
        nav_category = Content.objects.filter(
            user=user, 
            utopic=content.utopic, 
            status="approved",
            reply=None
        ).order_by("created")
        return render(
            request, 
            self.template_name, 
            dict(
                current_user=user,
                nav_category=nav_category,
                urloftopic=permlink,
                nameoflist=content.utopic,
                queryset=content,
                md_editor=True,
                reply_form=self.form_class,
            )
        )

    @method_decorator(login_required)
    def post(self, request, username, permlink, *args, **kwargs):
        parent_user = User.objects.get(username=username)
        parent_content = Content.objects.get(user=parent_user, permlink=permlink)
        reply_form = self.form_class(request.POST)
        if reply_form.is_valid():
            reply_form = reply_form.save(commit=False)
            reply_form.user = request.user
            reply_form.utopic = parent_content.utopic
            reply_form.language = parent_content.language
            reply_form.category = parent_content.category
            reply_form.tags = parent_content.tags
            reply_form.definition = parent_content.definition
            reply_form.status = parent_content.status
            reply_form.reply = parent_content
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
            return HttpResponse(
                json.dumps(
                    dict(
                        id=reply_form.id,
                        username=str(reply_form.user),
                        utopic_permlink=reply_form.utopic.permlink,
                        parent_permlink=reply_form.parent_permlink,
                        parent_user=str(reply_form.parent_user),
                        created=str(reply_form.created),
                        reply_count=reply_form.reply_count,
                        status=reply_form.status,
                        reply=reply_form.reply_id,
                        body=reply_form.body,
                        title=reply_form.title,
                        permlink=reply_form.permlink,
                        avatar_url=reply_form.user.githubauthuser.avatar_url,
                        get_absolute_url=reply_form.get_absolute_url
                        )
                    )
                )


@method_decorator(xframe_options_exempt, name="dispatch")
class Embed(Detail):
    template_name = "content-detail/embed.html"


class TreeDetail(TemplateView):
    template_name = "content-detail/tree.html"

    def get_context_data(self, hash, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context["queryset"] = Commit.objects.get(hash=hash)
        context["md_editor"] = True
        return context