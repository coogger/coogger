# django
from django.views.generic.base import TemplateView
from django.contrib.auth.models import User

# model
from core.cooggerapp.models import (Topic, UTopic, Content, Commit)


class UserTopic(TemplateView):
    "topic/@username"
    template_name = "utopic/contents-for-alt.html"

    def get_context_data(self, username, permlink, **kwargs):
        user = User.objects.get(username=username)
        utopic = UTopic.objects.get(user=user, permlink=permlink)
        contents = Content.objects.filter(
            user=user, 
            utopic=utopic, 
            status="approved", 
            reply=None).order_by("created")
        commits = Commit.objects.filter(utopic=utopic)
        context = super().get_context_data(**kwargs)
        if commits.exists():
            context["last_commit_created"] = commits[0].created        
        context["current_user"] = user
        context["queryset"] = contents
        context["utopic"] = utopic
        return context