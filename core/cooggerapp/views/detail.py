# django
from django.db.models import F
from django.contrib.auth.models import User
from django.views.decorators.clickjacking import xframe_options_exempt
from django.utils.decorators import method_decorator
from django.conf import settings
from django.core.paginator import (Paginator, EmptyPage, PageNotAnInteger)
from django.contrib.auth import authenticate
from django.http import Http404

# django class based
from django.views.generic.base import TemplateView

# core.cooggerapp models
from core.cooggerapp.models import (Content, Contentviews, UTopic)


class Detail(TemplateView):
    template_name = "content-detail/detail.html"

    def get_context_data(self, username, permlink, **kwargs):
        user = User.objects.get(username=username)
        content_obj = Content.objects.filter(user=user, permlink=permlink)
        content = content_obj[0]
        if not content_obj.exists():
            raise Http404
        content_views_obj = Contentviews.objects.filter(
            content=content,
            ip=self.get_ip_address()
        )
        if not content_views_obj.exists() and self.is_increase_view():
            content_obj.update(views=F("views") + 1)
            UTopic.objects.filter(
                user=user, 
                name=content.topic.name
            ).update(total_view=F("total_view")+1)
            Contentviews(content=content, ip=self.get_ip_address()).save()
        nav_category = Content.objects.filter(
            user=user, topic=content.topic, status="approved"
            ).order_by("created")
        urloftopic = permlink
        nameoflist = content.topic
        context = super().get_context_data(**kwargs)
        context["current_user"] = user
        context["nav_category"] = nav_category
        context["urloftopic"] = urloftopic
        context["nameoflist"] = nameoflist
        context["detail"] = content
        context["md_editor"] = True
        return context

    def get_ip_address(self):
        try:
            return self.request.META["HTTP_X_FORWARDED_FOR"].split(',')[-1].strip()
        except:
            return None

    def is_increase_view(self):
        if self.get_ip_address() is not None:
            return True
        return False


@method_decorator(xframe_options_exempt, name="dispatch")
class Embed(Detail):
    template_name = "content-detail/embed.html"