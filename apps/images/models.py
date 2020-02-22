from django.db.models import CharField, DateTimeField, ImageField, Model
from django.utils.timezone import now

from .configs import DefaultConfig


class Image(Model):
    title = CharField(
        blank=True,
        null=True,
        max_length=55,
        verbose_name="",
        help_text="Title | Optional",
    )
    image = ImageField(
        upload_to=DefaultConfig.folder_name, help_text="", verbose_name=""
    )
    created = DateTimeField(default=now, verbose_name="Created")

    @property
    def get_absolute_url(self):
        return f"{self.image.url}"
