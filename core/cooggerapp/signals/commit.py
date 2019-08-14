from django.db.models.signals import post_save
from django.dispatch import receiver

from ..models import Commit, UTopic


@receiver(post_save, sender=Commit)
def when_commit_create(sender, instance, created, **kwargs):
    if created and instance.status == "waiting":
        utopic = UTopic.objects.get(id=instance.utopic.id)
        utopic.open_contribution += 1
        utopic.save()
