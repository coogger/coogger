# django
from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now
from django.urls import reverse
from django.db.models import F
from django.template.loader import render_to_string
from django.utils.text import slugify

# model
from .utopic import UTopic

# editor md
from django_md_editor.models import EditorMdField

# choices
from core.cooggerapp.choices import make_choices, ISSUE_CHOICES

# python
import random


class Issue(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    utopic = models.ForeignKey(UTopic, on_delete=models.CASCADE)
    permlink = models.SlugField(max_length=200)
    title = models.CharField(max_length=55, help_text="Title", null=True, blank=True)
    body = EditorMdField(help_text="Your problem | question | or anything else")
    reply = models.ForeignKey("Issue", on_delete=models.CASCADE, null=True, blank=True)
    status = models.CharField(
        default="open", 
        choices=make_choices(ISSUE_CHOICES), 
        max_length=55, 
        help_text="Status",
        null=True, blank=True,
    )
    reply_count = models.IntegerField(default=0)
    issue_id = models.IntegerField(default=0)
    created = models.DateTimeField(default=now, verbose_name="Created")
    last_update = models.DateTimeField(default=now, verbose_name="Last update")

    class Meta:
        ordering = ["-created"]

    def save(self, *args, **kwargs):
        if self.reply is not None: # if make a comment
            self.status = None
            self.permlink = "re-" + self.user.username + "-re-" + \
                self.reply.user.username + "-" + slugify(self.reply.title.lower())
            self.title = self.reply.title
            reply_id = self.reply_id
            while True:
                query = self.__class__.objects.filter(id=reply_id)
                if query.exists():
                    query.update(
                            reply_count=(F("reply_count") + 1)
                        )
                    if query[0].reply is not None:
                        reply_id = query[0].reply_id
                    else:
                        break
                else:
                    break
        elif self.status == "open":
            self.permlink = slugify(self.title.lower())
            UTopic.objects.filter(
                user=self.user,
                name=self.utopic.name,
            ).update(open_issue=F("open_issue") + 1)
        while True:
            if self.__class__.objects.filter(
                utopic=self.utopic, 
                permlink=self.permlink
                ).exists():
                self.permlink = self.permlink + "-" + str(random.randrange(9999999))
            else:
                break
        self.issue_id = self.__class__.objects.filter(
            user=self.user,
            utopic=self.utopic,
            reply=None).count() + 1
        super().save(*args, **kwargs)

    @property
    def get_parent(self):
        return self.__class__.objects.get(id=self.reply_id)

    @property
    def parent_username(self):
        return self.get_parent.username

    @property
    def parent_permlink(self):
        return self.get_parent.permlink
    
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
        return self.user.username

    @property
    def topic_name(self):
        return self.utopic.name
