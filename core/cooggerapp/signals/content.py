#django
from django.dispatch import receiver
from django.db.models.signals import post_save, pre_delete
from django.db.models import F

#models
from ..models.content import Content
from ..models.commit import Commit
from ..models.topic import UTopic, Topic
from ..models.utils import send_mail, dor, is_comment

def update_topic(instance, iord):
    Topic.objects.filter(
            permlink=instance.utopic.permlink
        ).update(
            how_many=F("how_many") + iord
        )

def update_utopic(instance, iord):
    utopic = UTopic.objects.filter(
        user=instance.utopic.user,
        permlink=instance.utopic.permlink
    )
    utopic.update(
        how_many=F("how_many") + iord
    )
    if iord > 0:
        utopic.update(
            total_dor=F("total_dor") + dor(instance.body)
        )
    else:
        utopic.update(
            total_dor=F("total_dor") - dor(instance.body)
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
    if not is_comment(instance):
        update_topic(instance, - 1)
        update_utopic(instance, - 1)

@receiver(post_save, sender=Content)
def post_and_reply_created(sender, instance, created, **kwargs):
    if created:
        if not is_comment(instance):
            update_utopic(instance, + 1)
            commit(instance)
            if instance.status == "ready":
                update_topic(instance, + 1)
                send_mail(
                    subject=f"{ instance.user } publish a new content | coogger",
                    template_name="email/post.html",
                    context=dict(
                        get_absolute_url=instance.get_absolute_url,
                    ),
                    to=[u.user for u in instance.user.follow.follower if u.user.email],
                )
        else:
            user_list_to_email = list()
            for obj in instance.get_all_reply_obj():
                email = obj[0].user.email
                if (obj[0].user != instance.user) and (email) and (email not in user_list_to_email):
                    user_list_to_email.append(obj[0].user)
            send_mail(
                subject=f"{ instance.user } left a comment on your post | Coogger",
                template_name="email/reply.html",
                context=dict(
                    user=instance.user,
                    get_absolute_url=instance.get_absolute_url,
                ),
                to=user_list_to_email
            )
    else:
        update_fields = kwargs.get("update_fields")
        for field in update_fields:
            if field == "status":
                if instance.status == "ready":
                    update_topic(instance, + 1)
                else:
                    update_topic(instance, - 1)
                break