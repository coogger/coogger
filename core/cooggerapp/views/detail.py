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

# core.cooggerapp models
from ..models import Content, UTopic
from django_page_views.models import DjangoViews

# forms
from ..forms import NewContentReplyForm

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
        if request.is_ajax:
            parent_user = User.objects.get(username=username)
            parent_content = Content.objects.get(
                user=parent_user, 
                permlink=permlink
            )
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
                return HttpResponse(
                    json.dumps(
                        dict(
                            id=reply_form.id,
                            username=str(reply_form.user),
                            utopic_permlink=reply_form.utopic.permlink,
                            parent_permlink=reply_form.parent_permlink,
                            parent_username=reply_form.parent_username,
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