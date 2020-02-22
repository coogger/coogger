from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django.utils.translation import gettext as _

from .utils import ready_tags, second_convert


class CommonTopicModel(models.Model):
    name = models.CharField(
        max_length=50, verbose_name=_("Name"), help_text=_("Please, write topic name.")
    )
    permlink = models.SlugField(max_length=200)
    image_address = models.URLField(
        max_length=400, help_text=_("Add an Image Address"), blank=True, null=True
    )
    description = models.CharField(
        max_length=600, help_text=_("description of topic"), blank=True, null=True
    )
    tags = models.CharField(
        max_length=200,
        blank=True,
        null=True,
        verbose_name=_("Keyword"),
        help_text=_("Write your tags using spaces"),
    )
    address = models.URLField(
        blank=True, null=True, max_length=150, help_text=_("Add an address if it have")
    )
    how_many = models.PositiveIntegerField(
        default=0, verbose_name=_("How many content in")
    )

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        self.permlink = slugify(self.name)
        self.tags = ready_tags(self.tags)
        super().save(*args, **kwargs)


class Topic(CommonTopicModel):
    """ Global Topic Model """

    editable = models.BooleanField(
        default=True, verbose_name=_("Is it editable? | Yes/No")
    )

    class Meta:
        verbose_name_plural = _("Global Topic")
        ordering = ["-how_many"]
        unique_together = ["permlink"]

    def __str__(self):
        return self.permlink

    @property
    def global_topic(self):
        return True

    @property
    def get_absolute_url(self):
        return reverse("topic", kwargs=dict(permlink=self.permlink))


class UTopic(CommonTopicModel):
    """ Topic For Users """

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    total_dor = models.FloatField(
        default=0, verbose_name=_("Total duration all contents")
    )
    total_view = models.PositiveIntegerField(
        default=0, verbose_name=_("Total views all contents")
    )
    open_issue = models.PositiveIntegerField(
        default=0, verbose_name=_("Total count open issue")
    )
    closed_issue = models.PositiveIntegerField(
        default=0, verbose_name=_("Total count closed issue")
    )
    open_contribution = models.PositiveIntegerField(
        default=0, verbose_name=_("Total count open contributions")
    )
    closed_contribution = models.PositiveIntegerField(
        default=0, verbose_name=_("Total count closed contributions")
    )
    contributors = models.ManyToManyField(
        User, blank=True, related_name="utopic_contributors"
    )
    contributors_count = models.PositiveIntegerField(
        default=0, verbose_name=_("Total contributors count")
    )
    commit_count = models.PositiveIntegerField(
        default=0, verbose_name=_("Total commit count")
    )

    class Meta:
        verbose_name_plural = _("User Topic")
        ordering = ["-total_view", "-how_many"]
        unique_together = [["user", "permlink"]]

    def __str__(self):
        return str(self.get_absolute_url)

    @property
    def get_contributors(self):
        return self.contributors.filter(is_active=True)

    @property
    def global_topic(self):
        return False

    @property
    def get_absolute_url(self):
        return reverse(
            "detail-utopic",
            kwargs=dict(username=str(self.user), permlink=self.permlink),
        )

    @property
    def get_total_dor(self):
        times = str()
        for f, t in second_convert(self.total_dor).items():
            if t != 0:
                times += f" {t} {f} "
        return times
