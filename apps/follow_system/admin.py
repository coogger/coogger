from django.contrib.admin import ModelAdmin, site

from .models import Follow


class FollowAdmin(ModelAdmin):
    list_display = ["user"]
    list_display_links = list_display
    filter_horizontal = ["following"]


site.register(Follow, FollowAdmin)
