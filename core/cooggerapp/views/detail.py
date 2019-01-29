# django
from django.db.models import F
from django.contrib.auth import authenticate
from django.views.decorators.clickjacking import xframe_options_exempt
from django.utils.decorators import method_decorator

# django class based
from django.views.generic.base import TemplateView

# core.cooggerapp models
from core.cooggerapp.models import Content, Contentviews


class Detail(TemplateView):
    template_name = "detail/detail.html"

    def get_context_data(self, username, permlink, **kwargs):
        user = authenticate(username=username)
        content = Content.objects.filter(user=user, permlink=permlink)
        try:
            get_content = content[0]
        except IndexError:
            steem_post = dict(
                language = False,
                category = False,
                topic = False,
                status = "approved",
                views = False,
                steempost = True,
                user = user,
                permlink = permlink,
                get_absolute_url = f"/@{user}/{permlink}"
            )
            nav_category = None
            urloftopic = None
            nameoflist = None
            detail = steem_post
        else:
            try:
                ip = self.request.META["HTTP_X_FORWARDED_FOR"].split(',')[-1].strip()
            except:
                pass
            else:
                if not Contentviews.objects.filter(content=get_content, ip=ip).exists():
                    content.update(views=F("views") + 1)
                    Contentviews(content=get_content, ip=ip).save()
            topic = get_content.topic
            nav_category = Content.objects.filter(
                user=user, topic=topic, status="approved"
                ).order_by("created")
            urloftopic = permlink
            nameoflist = topic
            detail = get_content
        context = super(Detail, self).get_context_data(**kwargs)
        context["content_user"] = user
        context["nav_category"] = nav_category
        context["urloftopic"] = urloftopic
        context["nameoflist"] = nameoflist
        context["detail"] = detail
        return context


@method_decorator(xframe_options_exempt, name="dispatch")
class Embed(Detail):
    template_name = "detail/embed.html"
