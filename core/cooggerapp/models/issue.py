# django
from django.db.models import (
    Model, 
    ForeignKey, 
    CharField, 
    DateTimeField, 
    CASCADE, 
    IntegerField,
    SlugField
)
from django.contrib.auth.models import User
from django.utils.timezone import now
from django.urls import reverse
from django.db.models import F
from django.template.loader import render_to_string

# model
from .utopic import UTopic

# editor md
from django_md_editor.models import EditorMdField

# choices
from core.cooggerapp.choices import make_choices, ISSUE_CHOICES


class Issue(Model):
    user = ForeignKey(User, on_delete=CASCADE)
    utopic = ForeignKey(UTopic, on_delete=CASCADE)
    permlink = SlugField(max_length=200)
    title = CharField(max_length=55, help_text="Title", null=True, blank=True)
    body = EditorMdField()
    reply = ForeignKey("Issue", on_delete=CASCADE, null=True, blank=True)
    status = CharField(
        default="open", 
        choices=make_choices(ISSUE_CHOICES), 
        max_length=55, 
        help_text="Status",
        null=True, blank=True,
    )
    reply_count = IntegerField(default=0)
    created = DateTimeField(default=now, verbose_name="Created")
    last_update = DateTimeField(default=now, verbose_name="Last update")
    
    def __str__(self):
        return self.get_absolute_url()

    def get_absolute_url(self):
        return reverse("detail-issue", kwargs=dict(
            username=self.user.username, 
            topic=self.utopic.name,
            id=self.id,
            ))

    def save(self, *args, **kwargs):
        if self.reply is not None: # if make a comment
            self.status = None
        elif self.status == "open":
            UTopic.objects.filter(
                user=self.user,
                name=self.utopic.name,
            ).update(open_issue=F("open_issue") + 1)
        super().save(*args, **kwargs)
    
    @property
    def get_open_issues(self):
        return self.__class__.objects.filter(status="open", reply=None)

    @property
    def get_closed_issues(self):
        return self.__class__.objects.filter(status="closed", reply=None)
    
    @property
    def username(self):
        return self.user.username

    @property
    def topic_name(self):
        return self.utopic.name

