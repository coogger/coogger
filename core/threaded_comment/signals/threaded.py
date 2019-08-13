from django.db.models.signals import post_save
from django.dispatch import receiver


from ...cooggerapp.models import send_mail
from ..models import ThreadedComments

# TODO when_content_deleted pre_delete


@receiver(post_save, sender=ThreadedComments)
def when_create_comment(sender, instance, created, **kwargs):
    if created:
        obj = instance.get_top_obj
        obj.reply_count += 1
        obj.save()
        # send mail
        user_list_to_email = list()
        for obj in instance.get_all_reply_obj():
            email = obj[0].user.email
            if (
                (obj[0].user != instance.user)
                and (email)
                and (email not in user_list_to_email)
            ):
                user_list_to_email.append(obj[0].user)
        send_mail(
            subject=f"{ instance.user } left a comment on your post | Coogger",
            template_name="email/reply.html",
            context=dict(
                user=instance.user, get_absolute_url=instance.get_absolute_url
            ),
            to=user_list_to_email,
        )
