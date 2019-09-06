from django.db.models.signals import post_save
from django.dispatch import receiver

from ..models import Commit, UTopic, send_mail


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
