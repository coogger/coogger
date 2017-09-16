from django.contrib import admin
from blogapp.models import *

class ContentAdmin(admin.ModelAdmin):
    list_display = ["fields","title","time"]
    list_display_links = ["fields","title","time"]
    list_filter = ["fields","time"]
    search_fields = ["fields","title","tag","text"]
    prepopulated_fields = {"url":("title",)}
    class Media:
        js = ("js/my-admin-content.js",)
   

admin.site.register(Content,ContentAdmin)