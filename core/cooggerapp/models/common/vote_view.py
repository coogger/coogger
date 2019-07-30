#django
from django.db import models

#tags
from django_page_views.templatetags.django_page_views import views_count
from django_vote_system.templatetags.vote import upvote_count, downvote_count

class VoteView(models.Model):

    class Meta:
        abstract = True

    @property
    def model_name(self):
        return self.__class__.__name__.lower()

    @property
    def views(self):
        return views_count(self.__class__, self.id)

    @property
    def upvote_count(self):
        return upvote_count(self.__class__, self.id)

    @property
    def downvote_count(self):
        return downvote_count(self.__class__, self.id)