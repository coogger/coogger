from datetime import datetime

from core.cooggerapp.choices import REPORTS, make_choices
from django.contrib.auth.models import User
from django.db import models

from .content import Content


# TODO use content_type
class ReportModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="reporter")
    content = models.ForeignKey(
        Content, on_delete=models.CASCADE, verbose_name="reported person"
    )
    complaints = models.CharField(
        choices=make_choices(REPORTS), max_length=100, verbose_name="type of report"
    )
    add = models.CharField(
        blank=True,
        null=True,
        max_length=600,
        verbose_name="Can you give more information ?",
    )
    created = models.DateTimeField(default=datetime.now)
