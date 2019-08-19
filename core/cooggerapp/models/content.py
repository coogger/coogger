import mistune
from bs4 import BeautifulSoup
from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.text import slugify
from django_md_editor.models import EditorMdField

from core.cooggerapp.choices import LANGUAGES, STATUS_CHOICES, make_choices

from ...threaded_comment.models import AbstractThreadedComments
from .category import Category
from .common import Common, View, Vote
from .topic import UTopic
from .utils import dor, get_first_image, ready_tags, second_convert


class Content(AbstractThreadedComments, Common, View, Vote):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    permlink = models.SlugField(max_length=200)
    title = models.CharField(
        max_length=200,
        help_text="Be sure to choose the best title",
        null=True,
        blank=True,
    )
    body = EditorMdField(
        null=True,
        blank=True,
        verbose_name="",
        help_text="Your content | problem | question | or anything else",
    )
    utopic = models.ForeignKey(
        UTopic,
        on_delete=models.CASCADE,
        verbose_name="Your topic",
        help_text="Please, write your topic about your contents.",
    )
    language = models.CharField(
        max_length=30,
        choices=make_choices(LANGUAGES),
        help_text="The language of your content",
    )
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, help_text="select content category"
    )
    tags = models.CharField(
        max_length=200,
        verbose_name="Keywords",
        help_text="Write your tags using spaces, max:5",
    )
    image_address = models.URLField(null=True, blank=True)
    status = models.CharField(
        default="ready",
        max_length=30,
        choices=make_choices(STATUS_CHOICES),
        verbose_name="article's status",
        help_text="if your article isn't ready to publish yet, select 'not ready to publish'.",
    )
    contributors = models.ManyToManyField(
        User,
        blank=True,
        related_name="content_contributors"
    )
    contributors_count = models.PositiveIntegerField(
        default=0, verbose_name="Total contributors count"
    )

    class Meta:
        ordering = ["-created"]
        unique_together = [["user", "permlink"]]

    def __str__(self):
        return str(self.get_absolute_url)

    @property
    def get_absolute_url(self):
        return reverse(
            "content-detail",
            kwargs=dict(username=str(self.user), permlink=self.permlink),
        )

    @property
    def get_dor(self):
        times = ""
        for f, t in second_convert(dor(self.body)).items():
            if t != 0:
                times += f" {t}{f} "
        if times == "":
            return "0"
        return times

    def next_or_previous(self, next=True):
        queryset = self.__class__.objects.filter(user=self.user, utopic=self.utopic)
        index = list(queryset).index(queryset.get(id=self.id))
        if next:
            try:
                return queryset[index + 1]
            except IndexError:
                return None
        else:
            try:
                return queryset[index - 1]
            except (IndexError, AssertionError):
                return None

    @property
    def next_post(self):
        try:
            return self.next_or_previous().get_absolute_url
        except AttributeError:
            return False

    @property
    def previous_post(self):
        try:
            return self.next_or_previous(next=False).get_absolute_url
        except AttributeError:
            return False

    @property
    def other_content_of_this_topic(self):
        "left of content detail page section"
        return self.__class__.objects.filter(
            user=self.user, utopic=self.utopic
        ).order_by("created")

    def save(self, *args, **kwargs):
        self.image_address = get_first_image(self.body)
        self.permlink = slugify(self.title)
        self.tags = ready_tags(self.tags)
        self.last_update = timezone.now()
        super().save(*args, **kwargs)

    @property
    def description(self):
        renderer = mistune.Renderer(escape=False, parse_block_html=True)
        markdown = mistune.Markdown(renderer=renderer)
        return (
            BeautifulSoup(markdown(self.body), "html.parser")
            .text[0:200]
            .replace("\n", " ")
        )

    @property
    def get_last_commit(self):
        return self.commit_set.first()

    @property
    def get_contributors(self):
        return self.contributors.all()
