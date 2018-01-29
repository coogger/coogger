from django.contrib.admin import ModelAdmin,site
from apps.viewsapp.models import Contentviews

class ViewsAdmin(ModelAdmin):
    list_ = ["content_id","ip"]
    list_display = list_
    list_display_links = list_
    search_fields = list_

site.register(Contentviews, ViewsAdmin)
