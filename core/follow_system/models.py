from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import m2m_changed, post_save
from django.db.utils import IntegrityError
from django.dispatch import receiver

AUTH_USER_MODEL = getattr(settings, "AUTH_USER_MODEL", User)


class Follow(models.Model):
    user = models.OneToOneField(AUTH_USER_MODEL, on_delete=models.CASCADE)
    following = models.ManyToManyField(
        AUTH_USER_MODEL, blank=True, related_name="following"
    )
    created = models.DateTimeField(auto_now_add=True)

    @property
    def username(self):
        return str(self.user)

    @property
    def follower(self):
        return self.__class__.objects.filter(following=self.user.id)

    def is_follow(self, other_user):
        return bool(
            self.__class__.objects.filter(user=self.user).filter(
                following=other_user.id
            )
        )


@receiver(post_save, sender=User)
def create_user_follow(sender, instance, created, **kwargs):
    if created:
        Follow(user=instance).save()


@receiver(m2m_changed, sender=Follow.following.through)
def verify_follow_m2m(sender, **kwargs):
    oiou = kwargs.get("instance", None)
    action = kwargs.get("action", None)
    following = kwargs.get("pk_set", None)
    if action == "pre_add":
        for following_user_id in following:
            if following_user_id == oiou.user.id:
                raise IntegrityError("Can not be follow yourself")
            elif Follow.objects.filter(user=oiou.user).filter(
                following=following_user_id
            ):
                raise IntegrityError(
                    f"Follow with user {oiou.user}\
                      already exists for publisher {Follow.objects.get(user=oiou.user)}"
                )
