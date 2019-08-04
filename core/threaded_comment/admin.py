from django.contrib import admin

from .models import ThreadedComments


@admin.register(ThreadedComments)
class ThreadedCommentsAdmin(admin.ModelAdmin):
    pass
