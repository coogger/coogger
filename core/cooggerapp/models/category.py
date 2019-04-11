from django.db import models
from django.utils.text import slugify
from django_md_editor.models import EditorMdField


class Category(models.Model):
    name = models.CharField(max_length=50)
    template = EditorMdField(blank=True, null=True)

    def save(self, *args, **kwargs):
        self.name = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
