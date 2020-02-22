from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ObjectDoesNotExist
from django.db import models

from .utils import get_model

AUTH_USER_MODEL = getattr(settings, "AUTH_USER_MODEL", User)


class Bookmark(models.Model):
    user = models.ManyToManyField(AUTH_USER_MODEL)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey("content_type", "object_id")

    class Meta:
        unique_together = ["content_type", "object_id"]

    def __str__(self):
        return f"<{self.content_type.app_label} | {self.content_type.model} | {self.object_id}>"

    @property
    def how_many(self):
        try:
            obj = self.__class__.objects.get(
                content_type=self.content_type, object_id=self.object_id
            )
        except ObjectDoesNotExist:
            return 0
        return obj.user.count()

    @property
    def model_name(self):
        return self.model.__class__.__name__.lower()

    @property
    def model(self):
        return get_model(
            self.content_type.app_label, self.content_type.model, self.object_id
        )
