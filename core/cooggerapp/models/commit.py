from difflib import HtmlDiff

from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django_md_editor.models import EditorMdField

from ..choices import COMMIT_STATUS_CHOICES, make_choices
from .common import Common, View, Vote
from .content import Content
from .managers.commit import CommitManager
from .topic import UTopic
from .utils import get_new_hash

HtmlDiff._file_template = """<style type="text/css">%(styles)s</style>%(table)s"""
HtmlDiff._table_template = """
<table class="diff">
    <tbody>%(data_rows)s</tbody>
</table>
"""
HtmlDiff._styles = """
table.diff {font-family:Courier; border:medium;}
.diff_header {color:#99a3a4}
td.diff_header {text-align:center}
.diff tbody{display: block;}
.diff_next {background-color:#c0c0c0;display:none}
.diff_add {background-color:#aaffaa}
.diff_chg {background-color:#ffff77}
.diff_sub {background-color:#ffaaaa}
.diff [nowrap]{word-break: break-word;white-space: normal;width: 50%;}
"""


class Commit(Common, View, Vote):
    hash = models.CharField(max_length=256, unique=True, default=get_new_hash)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    utopic = models.ForeignKey(UTopic, on_delete=models.CASCADE)
    content = models.ForeignKey(Content, on_delete=models.CASCADE)
    body = EditorMdField()
    msg = models.CharField(max_length=150, default="Initial commit")
    created = models.DateTimeField(auto_now_add=True, verbose_name="Created")
    reply_count = models.PositiveIntegerField(default=0)
    status = models.CharField(
        max_length=100, default="approved", choices=make_choices(COMMIT_STATUS_CHOICES)
    )
    previous_commit = models.ForeignKey(
        "self", null=True, blank=True, on_delete=models.CASCADE
    )

    objects = CommitManager()

    class Meta:
        ordering = ["-created"]

    def __str__(self):
        return f"<Commit(content='{self.content}', msg='{self.msg}')>"

    @property
    def get_absolute_url(self):
        return reverse(
            "commit",
            kwargs=dict(
                username=str(self.user),
                topic_permlink=self.utopic.permlink,
                hash=self.hash,
            ),
        )

    @property
    def title(self):
        return self.msg

    @property
    def get_previous_commit(self):
        # NOTE just find and get previous_commit
        queryset = self.__class__.objects.filter(
            utopic=self.utopic, content=self.content, status="approved"
        )
        if self.status == "approved":
            # to commits page
            index = list(queryset).index(queryset.get(id=self.id))
            try:
                return queryset[index + 1]
            except IndexError:
                return None
        elif self.status == "waiting":
            try:
                return queryset[0]
            except IndexError:
                return None

    @property
    def body_change(self):
        previous_body = self.previous_commit.body
        if previous_body == self.body:
            previous_body = ""
        return HtmlDiff().make_file(previous_body.splitlines(), self.body.splitlines())
