#django
from django.dispatch import receiver
from django.db.models.signals import m2m_changed, post_save
from django.db import IntegrityError
from django.db.models import F

#django lib
from django_page_views.models import DjangoViews

#models
from ..models.topic import UTopic
from ..models.content import Content
from ..models.utils import is_comment

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
                    user=content.user,
                    permlink=content.utopic.permlink
                ).update(total_view=(F("total_view") + 1))

