from django.shortcuts import render
from django.db.models import F
from apps.viewsapp.models import Contentviews

def up_content_view(request,queryset):
    try:
        ip = request.META["HTTP_X_FORWARDED_FOR"].split(',')[-1].strip()
    except:
        ip = None
    if ip is None:
        return False
    if not Contentviews.objects.filter(content = queryset,ip = ip).exists():
        Contentviews(content = queryset,ip = ip).save()
        queryset.views = F("views") + 1
        queryset.save()
