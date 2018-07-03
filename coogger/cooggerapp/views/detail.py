#django
from django.contrib.auth.models import User
from django.db.models import F

#django class based
from django.views.generic.base import TemplateView

# cooggerapp models
from cooggerapp.models import Content,Contentviews

# cooggerapp views
from cooggerapp.views.tools import html_head

from cooggerapp.forms import ContentForm

class Detail(TemplateView):
    template_name = "detail/main_detail.html"
    ctof = Content.objects.filter

    def get_context_data(self,username,path, **kwargs):
        self.user = User.objects.filter(username = username)[0]
        self.path = path
        self.up_content_view() # ip aldık ve okuma sayısını 1 arttırdık
        queryset = self.permlinks_of_user()[0]
        context = super(Detail, self).get_context_data(**kwargs)
        context["head"] = html_head(queryset)
        context["content_user"] = queryset.user
        context["nav_category"] = self.lists_of_user()
        context["urloftopic"] = queryset.permlink
        context["nameoflist"] = queryset.topic
        context["detail"] = queryset
        return context

    def contents_of_user(self):
        return self.ctof(user = self.user)

    def permlinks_of_user(self):
        return self.contents_of_user().filter(permlink = self.path)

    def lists_of_user(self):
        permlinks = self.permlinks_of_user()[0]
        return self.contents_of_user().filter(topic = permlinks.topic,status="approved")

    def up_content_view(self):
        queryset = self.permlinks_of_user()
        Content.objects.filter(id = queryset[0].id).update(read = F("read")+1)
        try:
            ip = self.request.META["HTTP_X_FORWARDED_FOR"].split(',')[-1].strip()
        except:
            return False
        if not Contentviews.objects.filter(content = queryset[0],ip = ip).exists():
            Contentviews(content = queryset[0],ip = ip).save()
            queryset.update(views = F("views") + 1)
