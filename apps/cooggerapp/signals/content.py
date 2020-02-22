from django.db.models import F
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver

from ..models import (
    Commit, Content, Topic, UserProfile, UTopic, dor, send_mail
)
from ..templatetags.coogger_tags import hmanycontent
from .related.delete import (
    delete_related_bookmark, delete_related_views, delete_related_vote
)


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
        "when content create"
        utopic.update(
            total_dor=(F("total_dor") + dor(instance.body)),
            commit_count=(F("commit_count") + 1),
        )
    else:
        "when content delete"
        content_commit_count = Commit.objects.filter(content=instance).count()
        utopic.update(
            total_dor=(F("total_dor") - dor(instance.body)),
            commit_count=(F("commit_count") - content_commit_count),
        )


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
    delete_related_bookmark(sender, instance.id)
    delete_related_vote(sender, instance.id)
    delete_related_views(sender, instance.id)


@receiver(post_save, sender=Content)
def when_content_create(sender, instance, created, **kwargs):
    if created:
        # when user publish first content
        if hmanycontent(instance.user) == 0:
            userprofile = UserProfile.objects.get(user=instance.user)
            if userprofile.title == "user":
                userprofile.title = "author"
                userprofile.save()
        update_utopic(instance, +1)
        commit(instance)
        # permlink create
        instance.permlink = instance.generate_permlink()
        instance.save()
        if instance.status == "ready":
            update_topic(instance, +1)
            send_mail(
                subject=f"{ instance.user } published a new content | coogger",
                template_name="email/post.html",
                context=dict(get_absolute_url=instance.get_absolute_url),
                to=[u.user for u in instance.user.follow.follower if u.user.email],
            )
    else:
        update_fields = kwargs.get("update_fields", None)
        if update_fields and update_fields.__contains__("status"):
            if instance.status == "ready":
                update_topic(instance, +1)
            else:
                update_topic(instance, -1)
