from django.db.models.signals import pre_delete
from django.dispatch import receiver

from ...threaded_comment.models import ThreadedComments
from .related.delete import (
    delete_related_bookmark,
    delete_related_views,
    delete_related_vote,
)


@receiver(pre_delete, sender=ThreadedComments)
def when_threaded_comments_delete(sender, instance, **kwargs):
    delete_related_bookmark(sender, instance.id)
    delete_related_vote(sender, instance.id)
    delete_related_views(sender, instance.id)
