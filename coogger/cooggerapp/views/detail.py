# django
from django.contrib.auth.models import User
from django.db.models import F
from django.contrib.auth import authenticate

# django class based
from django.views.generic.base import TemplateView

# cooggerapp models
from cooggerapp.models import Content, Contentviews

# form
from cooggerapp.forms import ContentForm


class SteemPost():
    language = False
    category = False
    topic = False
    status = "approved"
    views = False
    read = False
    dor = False
    steempost = True

class Detail(TemplateView):
    # TODO: if content doesnt have on steem, it have to delete on coogger.
    template_name = "detail/main_detail.html"

    def get_context_data(self, username, path, **kwargs):
        self.user = authenticate(username=username)
        self.path = path
        try:
            self.up_content_view()
            queryset = self.permlinks_of_user()[0]
            nav_category = self.lists_of_user()
            urloftopic = queryset.permlink
            nameoflist = queryset.topic
            detail = queryset
        except IndexError:
            nav_category = None
            urloftopic = None
            nameoflist = None
            setattr(SteemPost, "user", self.user)
            setattr(SteemPost, "permlink", self.path)
            setattr(SteemPost, "status", "approved")
            detail = SteemPost
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
        return self.contents_of_user().filter(permlink=self.path)

    def lists_of_user(self):
        permlinks = self.permlinks_of_user()[0]
        return self.contents_of_user().filter(topic=permlinks.topic, status="approved")

    def up_content_view(self):
        queryset = self.permlinks_of_user()
        Content.objects.filter(id=queryset[0].id).update(read=F("read")+1)
        try:
            ip = self.request.META["HTTP_X_FORWARDED_FOR"].split(',')[-1].strip()
        except:
            return False
        if not Contentviews.objects.filter(content=queryset[0], ip=ip).exists():
            Contentviews(content=queryset[0], ip=ip).save()
            queryset.update(views=F("views") + 1)


class Embed(Detail):
    template_name = "detail/embed/embed.html"
