from datetime import datetime

from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import gettext as _

from apps.cooggerapp.choices import REPORTS, make_choices

from .content import Content


# TODO use content_type
class ReportModel(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name=_("reporter")
    )
    content = models.ForeignKey(
        Content, on_delete=models.CASCADE, verbose_name=_("reported person")
    )
    complaints = models.CharField(
        choices=make_choices(REPORTS),
        max_length=100,
        verbose_name=_("type of report"),
    )
    add = models.CharField(
        blank=True,
        null=True,
        max_length=600,
        verbose_name=_("Can you give more information ?"),
    )
    created = models.DateTimeField(default=datetime.now)
