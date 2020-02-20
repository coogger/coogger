from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext as _

from core.cooggerapp.choices import ISSUE_CHOICES, make_choices
from core.md_editor.models import EditorMdField

from ...threaded_comment.models import AbstractThreadedComments
from .common import Common, View, Vote
from .topic import UTopic
from .utils import dor, second_convert


class Issue(AbstractThreadedComments, Common, View, Vote):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    issue_id = models.PositiveIntegerField(default=0)
    title = models.CharField(
        max_length=200,
        help_text=_("Be sure to choose the best title"),
        null=True,
        blank=True,
    )
    utopic = models.ForeignKey(UTopic, on_delete=models.CASCADE)
    body = EditorMdField(
        null=True, blank=True, help_text=_("Your problem | question | or anything else")
    )
    status = models.CharField(
        default="open",
        choices=make_choices(ISSUE_CHOICES),
        max_length=55,
        help_text=_("Status"),
        null=True,
        blank=True,
    )

    class Meta:
        ordering = ["-created"]
        unique_together = [["user", "issue_id", "utopic"]]

    @property
    def get_absolute_url(self):
        return reverse(
            "detail-issue",
            kwargs=dict(
                username=str(self.utopic.user),
                utopic_permlink=self.utopic.permlink,
                issue_id=self.issue_id,
            ),
        )

    @property
    def get_dor(self):
        # TODO this function same in content.py models
        times = ""
        for f, t in second_convert(dor(self.body)).items():
            if t != 0:
                times += f" {t}{f} "
        if times == "":
            return "0"
        return times
