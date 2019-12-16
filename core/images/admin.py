# django
# model
from core.images.models import Image
from django.contrib.admin import ModelAdmin, site


class ImageAdmin(ModelAdmin):
    list_display = ["title", "image"]
    list_display_links = list_display
    search_fields = list_display


site.register(Image, ImageAdmin)
