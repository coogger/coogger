from django.contrib.admin import ModelAdmin, site

from .models import DjangoViews


class DjangoViewsAdmin(ModelAdmin):
    filter_horizontal = ("ips",)


site.register(DjangoViews, DjangoViewsAdmin)
