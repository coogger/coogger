# django
from django.dispatch import receiver
from django.db.models.signals import m2m_changed, post_save
from django.db import IntegrityError

# django lib
from django_page_views.models import DjangoViews

# models
from ..models.topic import UTopic, Topic
from ..models.content import Content

@receiver(post_save, sender=UTopic)
def global_topic_create(sender, instance, created, **kwargs):
    if created:
        try:
            Topic(name=instance.name).save()
        except IntegrityError:
            pass

@receiver(m2m_changed, sender=DjangoViews.ips.through)
def increase_total_view(sender, **kwargs):
    instance = kwargs.get("instance", None)
    action = kwargs.get("action", None)
    ips = kwargs.get("pk_set", None)
    if action == "pre_add":
        content = Content.objects.get(id=instance.object_id)
        for ip_id in ips:
            UTopic.objects.filter(
                user=content.user, 
                permlink=content.utopic.permlink
            ).update(total_view=(F("total_view") + 1))

