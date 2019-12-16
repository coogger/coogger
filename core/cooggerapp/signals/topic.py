from core.page_views.models import DjangoViews
from django.db.models import F
from django.db.models.signals import m2m_changed, post_save
from django.dispatch import receiver

from ..forms import UTopicForm
from ..models import Content, Topic, UTopic


@receiver(post_save, sender=UTopic)
def when_utopic_create(instance, created, **kwargs):
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
    # TODO move content detail class
    instance = kwargs.get("instance", None)
    action = kwargs.get("action", None)
    ips = kwargs.get("pk_set", None)
    if action == "pre_add" and instance.get_model == "content":
        content = Content.objects.get(id=instance.object_id)
        UTopic.objects.filter(
            user=content.user, permlink=content.utopic.permlink
        ).update(total_view=(F("total_view") + len(ips)))
