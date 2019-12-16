# admin
# models
from core.badge.models import Badges, UserBadge
from django.contrib import admin


@admin.register(Badges)
class BadgesAdmin(admin.ModelAdmin):
    pass


@admin.register(UserBadge)
class UserBadgeAdmin(admin.ModelAdmin):
    filter_horizontal = ["badge"]
