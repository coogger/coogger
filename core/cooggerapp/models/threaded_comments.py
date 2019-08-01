# django
from django.db import models
from django.contrib.auth.models import User
from django.db.models import F
from django.utils.text import slugify

# models
from .utils import is_comment

# python
import random


class ThreadedComments(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    permlink = models.SlugField(max_length=200)
    title = models.CharField(
        max_length=200,
        help_text="Be sure to choose the best title",
        null=True,
        blank=True,
    )
    reply = models.ForeignKey(
        "self", on_delete=models.CASCADE, null=True, blank=True, related_name="children"
    )
    reply_count = models.IntegerField(default=0)
    # depth = models.IntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True, verbose_name="Created")
    last_update = models.DateTimeField(auto_now_add=True, verbose_name="Last update")

    class Meta:
        ordering = ["-created"]
        abstract = True

    def __str__(self):
        return f"@{self.user}/{self.permlink}"

    @property
    def is_exists(self):
        # check with unique_together
        parameters = dict()
        for field in self._meta.unique_together:
            if isinstance(field, (tuple, list)):
                for f in field:
                    parameters[f] = getattr(self, f)
            else:
                parameters[field] = getattr(self, field)
        return self.__class__.objects.filter(**parameters).exists()

    def generate_permlink(self):
        def new_permlink():
            if is_comment(self):
                # if it is a comment
                return f"re-{str(self.user)}-re-{str(self.reply.user)}-{slugify(self.title.lower())}"
            return slugify(self.title.lower())

        if not self.permlink:
            self.permlink = new_permlink()
            while True:
                if self.is_exists:
                    self.permlink = self.permlink + "-" + str(random.randrange(9999999))
                else:
                    return self.permlink
        return self.permlink

    def save(self, *args, **kwargs):
        if is_comment(self) and not self.is_exists:
            # if it is a comment
            for obj in self.get_all_reply_obj():
                obj.update(reply_count=(F("reply_count") + 1))
        self.permlink = self.generate_permlink()
        super().save(*args, **kwargs)

    def get_all_reply_obj(self):
        reply_id = self.reply_id
        while True:
            query = self.__class__.objects.filter(id=reply_id)
            if query.exists():
                yield query
                if is_comment(query[0]):
                    reply_id = query[0].reply_id
                else:
                    break
            else:
                break

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
