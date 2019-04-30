from django.contrib.auth.models import User
from django.db import models
from django.utils.timezone import now

from core.cooggerapp.choices import make_choices, REPORTS

from .content import Content


class ReportModel(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name="reporter"
    )
    content = models.ForeignKey(
        Content, on_delete=models.CASCADE, verbose_name="reported person"
    )
    complaints = models.CharField(
        choices=make_choices(REPORTS), max_length=40, verbose_name="type of report"
    )
    add = models.CharField(
        blank=True,
        null=True,
        max_length=600,
        verbose_name="Can you give more information ?",
    )
    date = models.DateTimeField(default=now)

    @property
    def get_report(self):  # to api
        context = list()
        fields = ("complaints", "add", "date")
        queryset = self.__class__.objects.filter(content=self.content)
        for c in queryset:
            for f in fields:
                context.append({f: c.__getattribute__(f)})
        return context
