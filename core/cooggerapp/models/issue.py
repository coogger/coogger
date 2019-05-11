# django
from django.db.models import (Model, ForeignKey, CharField, DateTimeField, CASCADE)
from django.contrib.auth.models import User
from django.utils.timezone import now
from django.urls import reverse
from django.db.models import F

# model
from .utopic import UTopic

# editor md
from django_md_editor.models import EditorMdField

# choices
from core.cooggerapp.choices import make_choices, ISSUE_CHOICES


class Issue(Model):
    user = ForeignKey(User, on_delete=CASCADE)
    utopic = ForeignKey(UTopic, on_delete=CASCADE)
    title = CharField(max_length=55, help_text="Title")
    body = EditorMdField()
    status = CharField(default="open", choices=make_choices(ISSUE_CHOICES), max_length=55, help_text="Status")
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
        UTopic.objects.filter(
            user=self.user,
            name=self.utopic.name,
        ).update(open_issue=F("open_issue") + 1)
        super().save(*args, **kwargs)

