# django
from django.dispatch import receiver
from django.db.models.signals import post_save

# models
from ..models.issue import Issue
from ..models.topic import UTopic
from ..models.utils import send_mail

@receiver(post_save, sender=Issue)
def issue_counter(sender, instance, created, **kwargs):
    if created and instance.reply is None:
        #if is created and it is a issue not comment
        utopic = instance.utopic
        utopic = UTopic.objects.get(
            user=utopic.user, 
            permlink=utopic.permlink
        )
        utopic.open_issue = utopic.open_issue + 1
        utopic.closed_issue = utopic.closed_issue - 1
        utopic.save()
        if instance.user != instance.utopic.user:
            send_mail(
                subject=f"{instance.user} opened a new issue on your {instance.utopic.name} topic | coogger".title(), 
                template_name="email/new-issue.html", 
                context=dict(
                    form=instance,
                ),
                to=[instance.utopic.user]
            )
