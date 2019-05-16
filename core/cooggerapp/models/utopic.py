# django
from django.contrib.auth.models import User
from django.db import models, IntegrityError
from django.utils.text import slugify

# models
from .topic import Topic

# python
from contextlib import suppress


class UTopic(models.Model):
    """ Topic For Users """

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(
        max_length=50, verbose_name="Name", help_text="Please, write topic name."
    )
    image_address = models.URLField(
        max_length=400, help_text="Add an Image Address", blank=True, null=True
    )
    definition = models.CharField(
        max_length=600, help_text="Definition of topic", blank=True, null=True
    )
    tags = models.CharField(
        max_length=200,
        blank=True,
        null=True,
        verbose_name="Keyword",
        help_text="Write your tags using spaces",
    )
    address = models.URLField(
        blank=True, null=True, max_length=150, help_text="Add an address if it have"
    )
    total_dor = models.IntegerField(default=0, verbose_name="Total duration all contents")
    total_view = models.IntegerField(default=0, verbose_name="Total views all contents")
    open_issue = models.IntegerField(default=0, verbose_name="Total count open issue")
    closed_issue = models.IntegerField(default=0, verbose_name="Total count closed issue")

    class Meta:
        verbose_name_plural = "User Topic"
    
    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.name = slugify(self.name)
        if not self.__class__.objects.filter(user=self.user, name=self.name).exists():
            with suppress(IntegrityError):
                Topic(name=self.name).save()
        super().save(*args, **kwargs)

    @property
    def get_total_dor(self):
        second = self.total_dor
        def calculate(second):
            second = int(second)
            minutes = int(second / 60)
            second -= minutes * 60
            hours = int(second / (60 * 60))
            second -= hours * (60 * 60)
            days = int(second / (60 * 60 * 24))
            second -= days * (60 * 60 * 24)
            years = int(second / (60 * 60 * 24 * 365.25))
            second -= years * (60 * 60 * 24 * 365.25)
            return dict(years=years, days=days, hours=hours, minutes=minutes, second=int(second))
        times = str()
        for f, t in calculate(second).items():
            if t != 0:
                times += f" {t} {f} "
        return times