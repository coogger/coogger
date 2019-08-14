from django.db.models import F
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver

from ..models import Commit, Content, Topic, UTopic, dor, send_mail


def update_topic(instance, iord):
    Topic.objects.filter(permlink=instance.utopic.permlink).update(
        how_many=F("how_many") + iord
    )


def update_utopic(instance, iord):
    utopic = UTopic.objects.filter(
        user=instance.utopic.user, permlink=instance.utopic.permlink
    )
    utopic.update(how_many=F("how_many") + iord)
    if iord > 0:
        utopic.update(total_dor=F("total_dor") + dor(instance.body))
    else:
        utopic.update(total_dor=F("total_dor") - dor(instance.body))


def commit(instance):
    Commit(
        user=instance.user,
        utopic=instance.utopic,
        content=instance,
        body=instance.body,
        msg=f"{instance.title} Published.",
    ).save()


@receiver(pre_delete, sender=Content)
def when_content_delete(sender, instance, **kwargs):
    update_topic(instance, -1)
    update_utopic(instance, -1)


@receiver(post_save, sender=Content)
def post_and_reply_created(sender, instance, created, **kwargs):
    if created:
        update_utopic(instance, +1)
        commit(instance)
        if instance.status == "ready":
            update_topic(instance, +1)
            send_mail(
                subject=f"{ instance.user } publish a new content | coogger",
                template_name="email/post.html",
                context=dict(get_absolute_url=instance.get_absolute_url),
                to=[u.user for u in instance.user.follow.follower if u.user.email],
            )
    else:
        update_fields = kwargs.get("update_fields")
        try:
            for field in update_fields:
                if field == "status":
                    if instance.status == "ready":
                        update_topic(instance, +1)
                    else:
                        update_topic(instance, -1)
                    break
        except TypeError:
            pass
