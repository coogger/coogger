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
        null=True, blank=True,
    )
    issue_id = models.IntegerField(default=0)

    class Meta:
        ordering = ["-created"]

    @property
    def get_absolute_url(self):
        return reverse(
            "detail-issue", 
            kwargs=dict(
                username=str(self.user), 
                utopic_permlink=self.utopic.permlink,
                permlink=self.permlink
            )
        )

    def issue_save(self, *args, **kwargs):
        if self.reply is not None: # if make a comment
            self.status = None
        elif self.status == "open":
            UTopic.objects.filter(
                user=self.utopic.user,
                name=self.utopic.name,
            ).update(open_issue=F("open_issue") + 1)
        self.issue_id = self.__class__.objects.filter(
            utopic=self.utopic,
            reply=None).count() + 1
        super().save(*args, **kwargs)

    @property
    def get_open_issues(self):
        return self.__class__.objects.filter(
            utopic=self.utopic, 
            status="open", 
            reply=None
        )

    @property
    def get_closed_issues(self):
        return self.__class__.objects.filter(
            utopic=self.utopic, 
            status="closed", 
            reply=None
        )