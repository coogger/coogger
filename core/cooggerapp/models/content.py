# django
from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse

# models
from .category import Category
from .topic import UTopic
from .threaded_comments import ThreadedComments
from .utils import (
    second_convert, dor, 
    NextOrPrevious, 
    content_definition
)

# choices
from core.cooggerapp.choices import LANGUAGES, make_choices, STATUS_CHOICES

# 3.part models
from django_md_editor.models import EditorMdField

# 3.part tags
from django_page_views.templatetags.django_page_views import views_count
from django_vote_system.templatetags.vote import upvote_count, downvote_count

# python 
import random


class Content(ThreadedComments):
    body = EditorMdField(
        null=True, 
        blank=True, 
        verbose_name="",
        help_text="Your content | problem | question | or anything else"
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
        help_text="Write your tags using spaces, max:4",
    )
    definition = models.CharField(max_length=400, verbose_name="Definition of content")
    status = models.CharField(
        default="approved",
        max_length=30,
        choices=make_choices(STATUS_CHOICES),
        verbose_name="content's status",
    )
    mod = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="moderator",
    )  # is it necessary

    def __str__(self):
        return str(self.get_absolute_url)

    @property
    def get_absolute_url(self):
        return reverse("detail", kwargs=dict(username=str(self.user), permlink=self.permlink))

    @property
    def views(self):
        return views_count(self.__class__, self.id)

    @property
    def upvote_count(self):
        return upvote_count(self.__class__, self.id)

    @property
    def downvote_count(self):
        return downvote_count(self.__class__, self.id)

    @property
    def get_dor(self):
        times = "min"
        for f, t in second_convert(dor(self.body)).items():
            if t != 0:
                times += f" {t} {f} "
        if times == "min":
            return "min 0"
        return times

    def next_or_previous(self, next=True):
        filter_field = dict(
            user=self.user, utopic=self.utopic, reply=None
        )
        n_or_p = NextOrPrevious(self.__class__, filter_field, self.id)
        if next:
            return n_or_p.next_query
        return n_or_p.previous_query

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

    def save(self, *args, **kwargs):
        self.definition = content_definition(self.body)
        super().save(*args, **kwargs)