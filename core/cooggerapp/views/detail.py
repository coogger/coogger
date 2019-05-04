# django
from django.db.models import F
from django.contrib.auth import authenticate
from django.views.decorators.clickjacking import xframe_options_exempt
from django.utils.decorators import method_decorator
from django.conf import settings
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# django class based
from django.views.generic.base import TemplateView

# core.cooggerapp models
from core.cooggerapp.models import Content, Contentviews, Commit, Topic, UTopic

# views
from core.cooggerapp.views.users import Topic as UserTopicClass


class Detail(TemplateView):
    template_name = "detail/detail.html"

    def get_context_data(self, username, permlink, **kwargs):
        user = authenticate(username=username)
        content = Content.objects.filter(user=user, permlink=permlink)
        if content.exists():
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
        else:
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
            commits_count = None
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
    template_name = "detail/embed.html"


class Commits(UserTopicClass):
    template_name = "detail/commits.html"

    def get_context_data(self, username, topic, **kwargs):
        context = super().get_context_data(
            username, 
            topic, 
            **kwargs
            )
        del context["queryset"]
        return context

    def paginator(self, queryset):
        paginator = Paginator(queryset, settings.PAGE_SIZE)
        page = self.request.GET.get('page')
        try:
            contacts = paginator.page(page)
        except PageNotAnInteger:
            contacts = paginator.page(1)
        except EmptyPage:
            contacts = paginator.page(paginator.num_pages)
        return contacts

class CommitDetail(TemplateView):
    template_name = "detail/commit.html"

    def get_context_data(self, username, topic, hash, **kwargs):
        context = super().get_context_data(**kwargs)
        context["content_user"] = authenticate(username=username)
        context["commit"] = Commit.objects.filter(hash=hash)[0]
        return context
