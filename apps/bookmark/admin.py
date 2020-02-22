from django.contrib.admin import ModelAdmin, site

from .models import Bookmark


class BookmarkAdmin(ModelAdmin):
    filter_horizontal = ("user",)


site.register(Bookmark, BookmarkAdmin)
