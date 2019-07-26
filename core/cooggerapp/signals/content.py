# django
from django.dispatch import receiver
from django.db.models.signals import post_save

# models
from ..models.content import Content
from ..models.commit import Commit
from ..models.topic import UTopic
from ..models.utils import send_mail


@receiver(post_save, sender=Content)
def post_and_reply_created(sender, instance, created, **kwargs):
    if created:
        if instance.reply is None:
            #if it is a content
            send_mail(
                subject=f"{ instance.user } publish a new content | coogger", 
                template_name="email/post.html", 
                context=dict(
                    get_absolute_url=instance.get_absolute_url,
                ),
                to=[u.user for u in instance.user.follow.follower if u.user.email], 
            )
            Topic.objects.filter(
                permlink=instance.utopic.permlink
            ).update(
                how_many=(F("how_many") + 1)
            ) # increae how_many in Topic model
            UTopic.objects.filter(
                user=instance.utopic.user, 
                permlink=instance.utopic.permlink
            ).update(
                how_many=(F("how_many") + 1),
                total_dor=(F("total_dor") + dor(instance.body))
            ) # increase total dor in utopic
            Commit(
                user=instance.user,
                utopic=instance.utopic,
                content=instance,
                body=instance.body,
                msg=f"{instance.title} Published.",
            ).save()
        else:
            #if it is a reply
            email_list = list()
            for obj in instance.get_all_reply_obj():
                email = obj[0].user.email
                if (obj[0].user != instance.user) and (email) and (email not in email_list):
                    email_list.append(email)
            send_mail(
                subject=f"{ instance.user } left a comment on your post | Coogger", 
                template_name="email/reply.html", 
                context=dict(
                    user=instance.user,
                    get_absolute_url=instance.get_absolute_url,
                ),
                to=email_list
            )
        