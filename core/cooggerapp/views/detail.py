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
    # TODO: if content doesnt have on steem, it have to delete on coogger.
    template_name = "detail/detail.html"

    def get_context_data(self, topic, username, permlink, **kwargs):
        self.user = authenticate(username=username)
        self.permlink = permlink
        try:
            self.up_content_view()
            queryset = self.permlinks_of_user()[0]
            nav_category = self.lists_of_user()
            urloftopic = queryset.permlink
            nameoflist = queryset.topic
            detail = queryset
        except IndexError:
            steem_post = dict(
                language = False,
                category = False,
                topic = False,
                status = "approved",
                views = False,
                steempost = True,
                user = self.user,
                permlink = self.permlink,
                get_absolute_url = f"@{self.user}/{self.permlink}"
            )
            nav_category = None
            urloftopic = None
            nameoflist = None
            detail = steem_post
        context = super(Detail, self).get_context_data(**kwargs)
        context["content_user"] = self.user
        context["nav_category"] = nav_category
        context["urloftopic"] = urloftopic
        context["nameoflist"] = nameoflist
        context["detail"] = detail
        return context

    def contents_of_user(self):
        return Content.objects.filter(user=self.user)

    def permlinks_of_user(self):
        return self.contents_of_user().filter(permlink=self.permlink)

    def lists_of_user(self):
        permlinks = self.permlinks_of_user()[0]
        return self.contents_of_user().filter(topic=permlinks.topic, status="approved").order_by("id")

    def up_content_view(self):
        queryset = self.permlinks_of_user()
        try:
            ip = self.request.META["HTTP_X_FORWARDED_FOR"].split(',')[-1].strip()
        except:
            return False
        if not Contentviews.objects.filter(content=queryset[0], ip=ip).exists():
            Contentviews(content=queryset[0], ip=ip).save()
            queryset.update(views=F("views") + 1)

@method_decorator(xframe_options_exempt, name='dispatch')
class Embed(Detail):
    template_name = "detail/embed.html"
