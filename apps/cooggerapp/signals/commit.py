from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver

from ..models import Commit, UTopic, send_mail
from .related.delete import (
    delete_related_bookmark,
    delete_related_views,
    delete_related_vote,
)


@receiver(pre_delete, sender=Commit)
def when_commit_delete(sender, instance, **kwargs):
    delete_related_bookmark(sender, instance.id)
    delete_related_vote(sender, instance.id)
    delete_related_views(sender, instance.id)


@receiver(post_save, sender=Commit)
def when_commit_create(sender, instance, created, **kwargs):
    if created:
        if instance.status == "waiting":
            # when someone contribute a content
            utopic = UTopic.objects.get(id=instance.utopic.id)
            utopic.open_contribution += 1
            utopic.save()

            send_mail(
                subject=f"{ instance.user } contributed your article | coogger",
                template_name="email/contribute.html",
                context=dict(get_absolute_url=instance.get_absolute_url),
                to=[instance.content.user],
            )

        # NOTE previous commit is set
        instance.previous_commit = instance.get_previous_commit
        instance.save(update_fields=["previous_commit"])
