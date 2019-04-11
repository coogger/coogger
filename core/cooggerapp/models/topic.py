from django.db import models
from django.utils.text import slugify


class Topic(models.Model):
    """ Global Topic Model """

    name = models.SlugField(
        unique=True, max_length=50, help_text="Please, write topic name."
    )
    image_address = models.URLField(max_length=400, blank=True, null=True)
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
        blank=True, null=True, max_length=150, verbose_name="Add an address if it have"
    )
    editable = models.BooleanField(
        default=True, verbose_name="Is it editable? | Yes/No"
    )

    def save(self, *args, **kwargs):
        self.name = slugify(self.name)
        super(Topic, self).save(*args, **kwargs)

    def __str__(self):
        return self.name
