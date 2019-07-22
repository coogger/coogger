# django
from django.dispatch import receiver
from django.db.models.signals import post_save

# models
from ..models.issue import Issue
from ..models.topic import UTopic

@receiver(post_save, sender=Issue)
def issue_counter(sender, instance, created, **kwargs):
    if created and instance.reply is None:
        utopic = instance.utopic
        utopic = UTopic.objects.get(
            user=utopic.user, 
            permlink=utopic.permlink
        )
        utopic.open_issue = utopic.open_issue + 1
        utopic.closed_issue = utopic.closed_issue - 1
        utopic.save()
