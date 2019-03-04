# django
from django.db.models import F
from django.contrib.auth import authenticate
from django.views.decorators.clickjacking import xframe_options_exempt
from django.utils.decorators import method_decorator

# django class based
from django.views.generic.base import TemplateView

# core.cooggerapp models
from core.cooggerapp.models import Content, Contentviews, Commit, Topic, UTopic


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
            commits_count = None
        else:
            try:
                ip = self.request.META["HTTP_X_FORWARDED_FOR"].split(',')[-1].strip()
            except:
                pass
            else:
                if not Contentviews.objects.filter(content=get_content, ip=ip).exists():
                    content.update(views=F("views") + 1)
                    Contentviews(content=get_content, ip=ip).save()
            nav_category = Content.objects.filter(
                user=user, topic=get_content.topic, status="approved"
                ).order_by("created")
            urloftopic = permlink
            nameoflist = get_content.topic
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


class Commits(TemplateView):
    template_name = "detail/commits.html"

    def get_context_data(self, username, topic, **kwargs):
        user = authenticate(username=username)
        global_topic = Topic.objects.filter(name=topic)[0]
        contents = Content.objects.filter(user=user, topic=global_topic, status="approved")
        utopic = UTopic.objects.filter(user=user, name=topic)[0]
        context = super(Commits, self).get_context_data(**kwargs)
        commits = Commit.objects.filter(utopic=utopic)
        total_dor = 0
        for dor in [query.dor for query in contents]:
            total_dor += dor
        total_views = 0
        for views in [query.views for query in contents]:
            total_views += views
        context["content_user"] = user
        context["utopic"] = utopic
        context["commits_count"] = commits.count()
        context["last_commit"] = commits[len(commits)-1]
        context["commits"] = commits
        context["total_views"] = total_views
        context["total_dor"] = f"{round(total_dor, 3)} min"
        return context

class CommitDetail(TemplateView):
    template_name = "detail/commit.html"

    def get_context_data(self, username, topic, hash, **kwargs):
        context = super(CommitDetail, self).get_context_data(**kwargs)
        context["content_user"] = authenticate(username=username)
        context["commit"] = Commit.objects.filter(hash=hash)[0]
        return context
