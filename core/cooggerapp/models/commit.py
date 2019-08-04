from difflib import HtmlDiff

from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django_md_editor.models import EditorMdField

from .common import Common, View, Vote
from .content import Content
from .topic import UTopic
from .utils import NextOrPrevious, get_new_hash


class Commit(Common, View, Vote):
    hash = models.CharField(max_length=256, unique=True, default=get_new_hash)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    utopic = models.ForeignKey(UTopic, on_delete=models.CASCADE)  # is it necessary
    content = models.ForeignKey(Content, on_delete=models.CASCADE)
    body = EditorMdField()
    msg = models.CharField(max_length=150, default="Initial commit")
    created = models.DateTimeField(auto_now_add=True, verbose_name="Created")
    reply_count = models.PositiveIntegerField(default=0)

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
    def previous_commit(self):
        filter_field = dict(user=self.user, utopic=self.utopic, content=self.content)
        n_or_p = NextOrPrevious(self.__class__, filter_field, self.id)
        return n_or_p.previous_query

    @property
    def body_change(self):
        previous_commit = self.previous_commit
        if not previous_commit:
            return self.body
        HtmlDiff._file_template = (
            """<style type="text/css">%(styles)s</style>%(table)s"""
        )
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
        return HtmlDiff().make_file(
            previous_commit.body.splitlines(), self.body.splitlines()
        )
