from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import F
from django.utils.translation import gettext as _

AUTH_USER_MODEL = getattr(settings, "AUTH_USER_MODEL", User)


class CommonVote(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey("content_type", "object_id")

    class Meta:
        abstract = True
        # unique_together = [[]]


class VoteCount(CommonVote):
    upvote_count = models.IntegerField(default=0)
    downvote_count = models.IntegerField(default=0)

    def __str__(self):
        return f"<{self.object_id}. {self.content_type.app_label} | up = \
            {self.upvote_count}, down = {self.downvote_count}>"


class Vote(CommonVote):
    user = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE)
    status = models.BooleanField(default=True)
    # True = upvote, False = downvote

    def __str__(self):
        return f"<{self.user} | {self.object_id}. {self.content_type.app_label} \
            | model: {self.content_type.model}>"

    def get_model(self):
        return self.__class__.objects.filter(
            content_type=self.content_type, object_id=self.object_id
        )

    def save(self, *args, **kwargs):
        obj_filter = self.get_model().filter(user=self.user)
        vote_obj, created = VoteCount.objects.get_or_create(
            content_type=self.content_type, object_id=self.object_id
        )
        if obj_filter.filter(status=self.status).exists():
            raise ValidationError(_("This obj is already saved"))
        elif obj_filter.exists() and self.status != obj_filter[0].status:
            obj_filter.update(status=self.status)
            if self.status:
                "upvote"
                vote_obj.downvote_count = F("downvote_count") - 1
                vote_obj.upvote_count = F("upvote_count") + 1

            else:
                "downvote"
                vote_obj.downvote_count = F("downvote_count") + 1
                vote_obj.upvote_count = F("upvote_count") - 1
            vote_obj.save()
        else:
            if self.status:
                "upvote"
                vote_obj.upvote_count = F("upvote_count") + 1
            else:
                "downvote"
                vote_obj.downvote_count = F("downvote_count") + 1
            vote_obj.save()
            super().save(*args, **kwargs)
