from contextlib import suppress

from django.contrib.auth.models import User
from django.db import models, IntegrityError
from django.utils.text import slugify

from .topic import Topic


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

    class Meta:
        verbose_name_plural = "User Topic"
    
    def __str__(self):
        return self.name

    def get_total_dor(self):
        return f"{round(self.total_dor, 3)} min"

    def save(self, *args, **kwargs):
        self.name = slugify(self.name)
        if not self.__class__.objects.filter(user=self.user, name=self.name).exists():
            with suppress(IntegrityError):
                Topic(name=self.name).save()
            super().save(*args, **kwargs)