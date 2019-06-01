# django
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.db.models import F
from django.template.loader import render_to_string
from django.utils.text import slugify

# model
from .topic import UTopic
from core.django_threadedcomments_system.models import ThreadedComments

# editor md
from django_md_editor.models import EditorMdField

# choices
from core.cooggerapp.choices import make_choices, ISSUE_CHOICES

# python
import random


class Issue(ThreadedComments):
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

    def issue_save(self, *args, **kwargs):
        if self.reply is not None: # if make a comment
            self.status = None
        elif self.status == "open":
            UTopic.objects.filter(
                user=self.user,
                name=self.utopic.name,
            ).update(open_issue=F("open_issue") + 1)
        self.issue_id = self.__class__.objects.filter(
            user=self.user,
            utopic=self.utopic,
            reply=None).count() + 1
        super().save(*args, **kwargs)

    @property
    def get_open_issues(self):
        return self.__class__.objects.filter(
            user=self.user, 
            utopic=self.utopic, 
            status="open", 
            reply=None
        )

    @property
    def get_closed_issues(self):
        return self.__class__.objects.filter(
            user=self.user, 
            utopic=self.utopic, 
            status="closed", 
            reply=None
        )

    @property
    def username(self):
        return str(self.user)
    
    @property
    def utopic_permlink(self):
        return self.utopic.permlink

    @property
    def avatar_url(self):
        return self.user.githubauthuser.avatar_url
