from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver

from ..models import Issue, UTopic, send_mail
from .related.delete import (
    delete_related_bookmark,
    delete_related_views,
    delete_related_vote,
)


@receiver(pre_delete, sender=Issue)
def when_issue_delete(sender, instance, **kwargs):
    utopic = instance.utopic
    utopic = UTopic.objects.get(user=utopic.user, permlink=utopic.permlink)
    if instance.status == "open":
        utopic.open_issue = utopic.open_issue - 1
    else:
        utopic.closed_issue = utopic.closed_issue - 1
    utopic.save()
    delete_related_bookmark(sender, instance.id)
    delete_related_vote(sender, instance.id)
    delete_related_views(sender, instance.id)


@receiver(post_save, sender=Issue)
def issue_counter(sender, instance, created, **kwargs):
    if created:
        utopic = instance.utopic
        utopic = UTopic.objects.get(user=utopic.user, permlink=utopic.permlink)
        utopic.open_issue = utopic.open_issue + 1
        utopic.save()
        if instance.user != instance.utopic.user:
            send_mail(
                subject=f"{instance.user} opened a new issue on your {instance.utopic.name} topic | coogger".title(),
                template_name="email/new-issue.html",
                context=dict(form=instance),
                to=[instance.utopic.user],
            )
