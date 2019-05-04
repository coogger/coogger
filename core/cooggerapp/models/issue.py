# django
from django.db.models import (Model, ForeignKey, CharField, DateTimeField)
from django.contrib.auth.models import User
from django.utils.timezone import now

# model
from .utopic import UTopic

# editor md
from django_md_editor.models import EditorMdField

# choices
from core.cooggerapp.choices import make_choices, ISSUE_CHOICES


class Issue(Model):
    user = ForeignKey(User, on_delete=models.CASCADE)
    utopic = ForeignKey(UTopic, on_delete=models.CASCADE)
    title = CharField(max_length=55, help_text="Title")
    body = EditorMdField()
    status = CharField(choices=make_choices(ISSUE_CHOICES), max_length=55, help_text="Status")
    created = DateTimeField(default=now, verbose_name="Created")