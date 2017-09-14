from django.contrib import admin
from blogapp.models import *

class ContentAdmin(admin.ModelAdmin):
    list_display = ["issue","title","time"]
    list_display_links = ["issue","title","time"]
    list_filter = ["issue","time"]
    search_fields = ["issue","title","tag","text"]
    prepopulated_fields = {"url":("title",)}
   

admin.site.register(Content,ContentAdmin)