# django
from django.contrib.auth.models import User
from django.db import models
from django.utils.timezone import now

# 3.part
from django_md_editor.models import EditorMdField

# models
from .utopic import UTopic
from .content import Content

# utils
from .utils import get_new_hash

# python
from difflib import HtmlDiff


class Commit(models.Model):
    hash = models.CharField(max_length=256, unique=True, default=get_new_hash)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    utopic = models.ForeignKey(UTopic, on_delete=models.CASCADE)  # is it necessary
    content = models.ForeignKey(Content, on_delete=models.CASCADE)
    body = EditorMdField()
    msg = models.CharField(max_length=150, default="Initial commit")
    created = models.DateTimeField(default=now, verbose_name="Created")

    class Meta:
        ordering = ["-created"]

    def __str__(self):
        return f"<Commit(content='{self.content}', msg='{self.msg}')>"

    @property
    def previous_commit(self):
        commits = self.__class__.objects.filter(
            user=self.user, utopic=self.utopic, content=self.content
        )
        index = list(commits).index(commits.filter(id=self.id)[0]) + 1
        try:
            return commits[index]
        except (IndexError):
            return False

    @property
    def body_change(self):
        previous_commit = self.previous_commit
        if not previous_commit:
            return self.body
        after = list()
        before = list()

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
    
    @property
    def content_absolute_url(self):
        return self.content.get_absolute_url
    
    @property
    def username(self):
        return self.user.username

    @property
    def topic_name(self):
        return self.utopic.name