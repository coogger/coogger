from django.db.models import F
from django.db.models.signals import m2m_changed, post_save
from django.dispatch import receiver
from django_page_views.models import DjangoViews

from ..forms import UTopicForm
from ..models.content import Content
from ..models.topic import Topic, UTopic
from ..models.utils import is_comment


@receiver(post_save, sender=UTopic)
def global_topic_create(instance, created, **kwargs):
    if created:
        # issue 101 and when utopic create, topic create too
        get_global_topic, created = Topic.objects.get_or_create(
            name=instance.name.lower()
        )
        if not get_global_topic.editable:
            for field in UTopicForm._meta.fields:
                if getattr(instance, field, None) == None:
                    setattr(instance, field, getattr(get_global_topic, field))
            instance.save()


@receiver(m2m_changed, sender=DjangoViews.ips.through)
def increase_utopic_view(sender, **kwargs):
    instance = kwargs.get("instance", None)
    action = kwargs.get("action", None)
    ips = kwargs.get("pk_set", None)
    if action == "pre_add" and instance.get_model == "content":
        content = Content.objects.get(id=instance.object_id)
        if not is_comment(content):
            for ip_id in ips:
                UTopic.objects.filter(
                    user=content.user, permlink=content.utopic.permlink
                ).update(total_view=(F("total_view") + 1))
