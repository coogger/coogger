from django.contrib import admin

from .models import ThreadedComments


@admin.register(ThreadedComments)
class ThreadedCommentsAdmin(admin.ModelAdmin):
    # pass
    # def save_model(self, request, obj, form, change):
    #        super().save_model(request, obj, form, change)
