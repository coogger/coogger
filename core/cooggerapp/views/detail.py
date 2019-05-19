# django
from django.db.models import F
from django.contrib.auth.models import User
from django.views.decorators.clickjacking import xframe_options_exempt
from django.utils.decorators import method_decorator
from django.conf import settings
from django.core.paginator import (Paginator, EmptyPage, PageNotAnInteger)
from django.http import Http404

# django class based
from django.views.generic.base import TemplateView

# core.cooggerapp models
from core.cooggerapp.models import (Content, Contentviews, UTopic)


class Detail(TemplateView):
    template_name = "content-detail/detail.html"

    def get_context_data(self, username, permlink, **kwargs):
        user = User.objects.get(username=username)
        content = Content.objects.filter(user=user, permlink=permlink)
        if not content.exists():
            raise Http404
        if not Contentviews.objects.filter(
            content=content[0], 
            ip=self.get_ip_address()
            ).exists() and self.is_increase_view():
            content.update(views=F("views") + 1)
            UTopic.objects.filter(
                user=user, 
                name=content[0].topic.name
            ).update(total_view=F("total_view")+1)
            Contentviews(content=content[0], ip=self.get_ip_address()).save()
        nav_category = Content.objects.filter(
            user=user, topic=content[0].topic, status="approved"
            ).order_by("created")
        urloftopic = permlink
        nameoflist = content[0].topic
        detail = content[0]
        context = super().get_context_data(**kwargs)
        context["content_user"] = user
        context["nav_category"] = nav_category
        context["urloftopic"] = urloftopic
        context["nameoflist"] = nameoflist
        context["detail"] = detail
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