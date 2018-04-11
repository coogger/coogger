#django
from django.contrib.auth.models import User
from django.db.models import F

#django class based
from django.views.generic.base import TemplateView

# cooggerapp models
from apps.cooggerapp.models import Content,Contentviews

# cooggerapp views
from apps.cooggerapp.views.tools import html_head
from apps.cooggerapp.views.users import is_follow

class Detail(TemplateView):
    template_name = "apps/cooggerapp/detail/main_detail.html"
    ctof = Content.objects.filter

    def get_context_data(self,username,path, **kwargs):
        user = User.objects.filter(username = username)[0]
        utopic = self.ctof(user = user, permlink = path)[0].content_list
        queryset = self.ctof(user = user, content_list = utopic, permlink = path)[0]
        content_user = queryset.user
        nav_category = self.ctof(user = content_user,content_list = utopic)
        self.up_content_view(queryset) # ip aldık ve okuma sayısını 1 arttırdık
        context = super(Detail, self).get_context_data(**kwargs)
        context["head"] = html_head(queryset)
        context["content_user"] = content_user
        context["nav_category"] = nav_category
        context["urloftopic"] = queryset.permlink
        context["nameoflist"] = utopic
        context["is_follow"] = is_follow(self.request,user)
        context["detail"] = queryset
        context["global_hashtag"] = [i for i in queryset.tag.split(" ") if i != ""]
        return context

    def up_content_view(self,queryset):
        Content.objects.filter(id = queryset.id).update(read = F("read")+1)
        try:
            ip = self.request.META["HTTP_X_FORWARDED_FOR"].split(',')[-1].strip()
        except:
            ip = None
        if ip is None:
            return False
        if not Contentviews.objects.filter(content = queryset,ip = ip).exists():
            Contentviews(content = queryset,ip = ip).save()
            queryset.views = F("views") + 1
            queryset.save()
