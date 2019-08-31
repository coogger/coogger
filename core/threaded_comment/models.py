from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.db.models import F
from django.urls import reverse

from ..cooggerapp.models.common import Common, View, Vote
from ..cooggerapp.models.utils import get_first_image


class AbstractThreadedComments(models.Model):
    reply_count = models.PositiveIntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True, verbose_name="Created")
    updated = models.DateTimeField(
        auto_now=True,
        verbose_name="Last update"
    )

    class Meta:
        abstract = True


class AllProperties(models.Model):
    class Meta:
        abstract = True

    @property
    def get_parent(self):
        if self.reply is None:
            return self
        return self.__class__.objects.get(id=self.reply_id)

    @property
    def parent_user(self):
        return self.get_parent.user

    @property
    def parent_permlink(self):
        return self.get_parent.permlink

    def is_threaded_comments(self, obj=None):
        if obj is None:
            return self.reply is not None
        return obj.reply is not None

    @property
    def get_top_obj(self):
        if not self.is_threaded_comments():
            return self.content_type.model_class().objects.get(id=self.object_id)
        for obj in self.get_all_reply_obj():
            if not self.is_threaded_comments(obj[0]):
                first_reply = obj[0]
                return first_reply.content_type.model_class().objects.get(
                    id=first_reply.object_id
                )


class ThreadedComments(AbstractThreadedComments, AllProperties, Common, Vote, View):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    permlink = models.PositiveIntegerField(default=99999999999999)
    body = models.TextField()
    image_address = models.URLField(null=True, blank=True)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey("content_type", "object_id")
    reply = models.ForeignKey(
        "self", on_delete=models.CASCADE, null=True, blank=True, related_name="children"
    )
    depth = models.PositiveIntegerField(default=0)
    to = models.ForeignKey(User, on_delete=models.CASCADE, related_name="to")

    class Meta:
        ordering = ["-created"]
        unique_together = [["user", "permlink"]]

    def __str__(self):
        return f"/@{self.user}/{self.permlink}"

    @property
    def get_absolute_url(self):
        return reverse(
            "reply-detail", kwargs=dict(username=str(self.user), permlink=self.permlink)
        )

    @property
    def is_exists(self):
        return self.__class__.objects.filter(
            user=self.user, permlink=self.permlink
        ).exists()

    def generate_permlink(self):
        if not self.is_exists:
            queryset = self.__class__.objects.filter(user=self.user)
            if not queryset.exists():
                return 1
            else:
                return queryset.first().permlink + 1
        return self.permlink

    def save(self, *args, **kwargs):
        if self.is_threaded_comments() and not self.is_exists:
            "It is not working when update"
            for obj in self.get_all_reply_obj():
                obj.update(reply_count=(F("reply_count") + 1))
        self.image_address = get_first_image(self.body)
        self.permlink = self.generate_permlink()
        self.to = self.get_to()
        self.depth = self.get_parent_count()
        super().save(*args, **kwargs)

    def get_all_reply_obj(self):
        reply_id = self.reply_id
        while True:
            query = self.__class__.objects.filter(id=reply_id)  # get parent
            if query.exists():
                yield query
                if self.is_threaded_comments(query[0]):
                    reply_id = query[0].reply_id
                else:
                    break
            else:
                break

    def get_parent_count(self):
        reply_id = self.reply_id
        parent_count = 0
        while reply_id:
            try:
                parent = ThreadedComments.objects.get(id=reply_id)
            except IndexError:
                break
            else:
                if parent:
                    parent_count += 1
                    if parent.is_threaded_comments():
                        reply_id = parent.reply_id
                    else:
                        break
                else:
                    break
        return parent_count

    @property
    def is_reply(self):
        return True

    def get_to(self):
        model_name = self.content_type.model
        app_label = self.content_type.app_label
        model = ContentType.objects.get(app_label=app_label, model=model_name)
        return model.get_object_for_this_type(id=self.object_id).user
