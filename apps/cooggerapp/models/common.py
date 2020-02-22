from django.contrib.contenttypes.models import ContentType
from django.db import models

from apps.page_views.templatetags.django_page_views import views_count
from apps.vote_system.templatetags.vote import downvote_count, upvote_count


class Common(models.Model):
    class Meta:
        abstract = True

    @property
    def content_type_obj(self):
        return ContentType.objects.get_for_model(self)

    @property
    def app_label(self):
        return self.content_type_obj.app_label

    @property
    def model_name(self):
        return self.content_type_obj.model


class Vote(models.Model):
    class Meta:
        abstract = True

    @property
    def upvote_count(self):
        return upvote_count(self.__class__, self.id)

    @property
    def downvote_count(self):
        return downvote_count(self.__class__, self.id)


class View:
    id = None

    class Meta:
        abstract = True

    @property
    def views(self):
        return views_count(self.__class__, self.id)
