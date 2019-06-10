# django
from django.db import models, IntegrityError
from django.utils.text import slugify
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from django.db.models import F

# models
from django_page_views.models import DjangoViews

# python
from contextlib import suppress

# utils
from .utils import second_convert

class CommonTopicModel(models.Model):
    name = models.CharField(
        max_length=50, verbose_name="Name", help_text="Please, write topic name."
    )
    permlink = models.SlugField(max_length=200)
    image_address = models.URLField(
        max_length=400, help_text="Add an Image Address", blank=True, null=True
    )
    definition = models.CharField(
        max_length=600, help_text="Definition of topic", blank=True, null=True
    )
    tags = models.CharField(
        max_length=200,
        blank=True,
        null=True,
        verbose_name="Keyword",
        help_text="Write your tags using spaces",
    )
    address = models.URLField(
        blank=True, null=True, max_length=150, help_text="Add an address if it have"
    )
    how_many = models.IntegerField(default=0, verbose_name="How many content in")

    class Meta:
        abstract = True

    def __str__(self):
        return self.name


class Topic(CommonTopicModel):
    """ Global Topic Model """
    editable = models.BooleanField(
        default=True, verbose_name="Is it editable? | Yes/No"
    )

    class Meta:
        verbose_name_plural = "Global Topic"
        ordering = ["-how_many"]
        unique_together = ["permlink"]


    def save(self, *args, **kwargs):
        self.permlink = slugify(self.name)
        super().save(*args, **kwargs)

    @property
    def get_absolute_url(self):
        return reverse(
            "topic",
            kwargs=dict(
                permlink=self.permlink
            )
        )


class UTopic(CommonTopicModel):
    """ Topic For Users """
    # TODO if topic name is changed, then must change the permlink
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    total_dor = models.FloatField(default=0, verbose_name="Total duration all contents")
    total_view = models.IntegerField(default=0, verbose_name="Total views all contents")
    open_issue = models.IntegerField(default=0, verbose_name="Total count open issue")
    closed_issue = models.IntegerField(default=0, verbose_name="Total count closed issue")

    class Meta:
        verbose_name_plural = "User Topic"
        ordering = ["-how_many"]
        unique_together = [["user", "permlink"]]

    @property
    def get_absolute_url(self):
        return reverse(
            "detail-utopic",
            kwargs=dict(
                username=str(self.user),
                permlink=self.permlink
            )
        )

    def save(self, *args, **kwargs):
        try:
            Topic(name=self.name).save()
        except IntegrityError:
            pass
        self.permlink = slugify(self.name)
        super().save(*args, **kwargs)

    @property
    def get_total_dor(self):
        times = str()
        for f, t in second_convert(self.total_dor).items():
            if t != 0:
                times += f" {t} {f} "
        return times

@receiver(m2m_changed, sender=DjangoViews.ips.through)
def increase_total_view(sender, **kwargs):
    instance = kwargs.get("instance", None)
    action = kwargs.get("action", None)
    ips = kwargs.get("pk_set", None)
    if action == "pre_add":
        Content = ContentType.objects.get(app_label="cooggerapp", model="content").model_class()
        content = Content.objects.get(id=instance.object_id)
        for ip_id in ips:
            UTopic.objects.filter(
                user=content.user, 
                permlink=content.utopic.permlink
            ).update(total_view=(F("total_view") + 1))