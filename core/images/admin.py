# django
# model
from django.contrib.admin import ModelAdmin, site

from core.images.models import Image


class ImageAdmin(ModelAdmin):
    list_display = ["title", "image"]
    list_display_links = list_display
    search_fields = list_display


site.register(Image, ImageAdmin)
