# django
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.db.models import F
from django.template.loader import render_to_string
from django.utils.text import slugify

# model
from .topic import UTopic
from .threaded_comments import ThreadedComments
from .common.vote_view import VoteView
from .utils import second_convert, dor

# editor md
from django_md_editor.models import EditorMdField

# choices
from core.cooggerapp.choices import make_choices, ISSUE_CHOICES

# python
import random


class Issue(ThreadedComments, VoteView):
    utopic = models.ForeignKey(
        UTopic,
        on_delete=models.CASCADE
        )
    body = EditorMdField(
        null=True,
        blank=True,
        help_text="Your problem | question | or anything else")
    status = models.CharField(
        default="open",
        choices=make_choices(ISSUE_CHOICES),
        max_length=55,
        help_text="Status",
        null=True,
        blank=True,
    )
    issue_id = models.IntegerField(default=0)

    class Meta(ThreadedComments.Meta):
        unique_together = [["utopic", "permlink"]]
        # this line causes IntegrityError error during super() and then work create a new permlink

    @property
    def get_absolute_url(self):
        return reverse(
            "detail-issue",
            kwargs=dict(
                username=str(self.utopic.user),
                utopic_permlink=self.utopic.permlink,
                permlink=self.permlink
            )
        )

    @property
    def get_dor(self):
        #TODO this function same in content.py models
        times = ""
        for f, t in second_convert(dor(self.body)).items():
            if t != 0:
                times += f" {t}{f} "
        if times == "":
            return "0"
        return times

