from django.db.models import F
from django.db.models.signals import m2m_changed, post_save
from django.dispatch import receiver
from django_page_views.models import DjangoViews

from ..forms import UTopicForm
from ..models import Content, Topic, UTopic
from ..views.utils import check_redirect_exists


@receiver(post_save, sender=UTopic)
def when_utopic_create(instance, created, **kwargs):
    if created:
        obj, is_exists = check_redirect_exists(old_path=instance.get_absolute_url)
        if is_exists:
            import random

            instance.permlink += str(random.randrange(99999999))
            instance.save()
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
