from django.db import models
from apps.cooggerapp.models import Content


class Contentviews(models.Model):
    content = models.ForeignKey(Content ,on_delete=models.CASCADE)
    ip = models.GenericIPAddressField()

    class Meta:
        app_label = 'viewsapp'
