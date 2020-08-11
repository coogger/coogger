from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.db.models.signals import m2m_changed
from django.db.utils import IntegrityError
from django.dispatch import receiver

from apps.ip.models import IpModel


class DjangoViews(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey("content_type", "object_id")
    ips = models.ManyToManyField(IpModel)
    views_count = models.IntegerField(default=0)

    def __str__(self):
        return f"<{self.get_app_label} ({self.object_id}) \
            | model: {self.get_model} | views_count: {self.views_count}>"

    @property
    def get_app_label(self):
        return self.content_type.app_label

    @property
    def get_model(self):
        return self.content_type.model


@receiver(m2m_changed, sender=DjangoViews.ips.through)
def verify_views_m2m(sender, **kwargs):
    instance = kwargs.get("instance", None)
    action = kwargs.get("action", None)
    ips = kwargs.get("pk_set", None)
    if action == "pre_add":
        for ip_id in ips:
            model = DjangoViews
            query = model.objects.filter(
                content_type=instance.content_type,
                object_id=instance.object_id,
            )
            if query.filter(ips=ip_id).exists():
                raise IntegrityError(
                    f"<Already save {instance.content_type.model} id:{instance.object_id}>"
                )
    instance.views_count = instance.ips.all().count()
    instance.save(update_fields=["views_count"])
