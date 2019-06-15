from django.contrib.admin import ModelAdmin, site

#models
from core.cooggerapp.models import (
    Content, 
    SearchedWords,
    ReportModel, 
    UserProfile, 
    Topic, 
    Commit, 
    UTopic, 
    Category,
    Issue,
)

#choices
from core.cooggerapp.choices import *

# python
import datetime


class ContentAdmin(ModelAdmin):
    list_display = ["user","permlink", "mod", "reply"]
    list_display_links = list_display
    list_filter = ["status"]
    search_fields = ["title", "body", "permlink"]
    fields = (
        ("user"),
        ("category", "language", "utopic"),
        ("title", "permlink"),
        ("reply"),
        ("definition"),
        ("body"),
        ("tags", "status"),
        ("reply_count"),
    )

    def save_model(self, request, obj, form, change):
        obj.mod = request.user
        super().save_mode(request, obj, form, change)


class SearchedWordsAdmin(ModelAdmin):
    list_display = ["word","hmany"]
    list_display_links = list_display
    search_fields = list_display


class UserProfileAdmin(ModelAdmin):
    list_display = ["user"]
    list_display_links = list_display
    filter_horizontal = ("address", )
    

class TopicAdmin(ModelAdmin):
    list_ = ["name", "tags", "editable"]
    list_display = list_
    list_display_links = list_
    list_filter = ["editable"]
    search_fields = ["name","definition"]
    fields = (
        ("name", "tags"),
        ("definition"),
        ("image_address"),
        ("address"),
        ("editable"),
    )


class CommitAdmin(ModelAdmin):
    list_display = ["content", "utopic"]
    list_display_links = ["content", "utopic"]
    list_filter = ["created"]
    search_fields = ["msg", "body"]


class UtopicAdmin(ModelAdmin):
    list_display = ["user", "name"]
    list_display_links = ["user", "name"]
    search_fields = ["name"]
    fields = (
        ("user"),
        ("name"),
        ("image_address"),
        ("definition"),
        ("tags"),
        ("address"),
        (
            "total_dor", 
            "total_view", 
            "open_issue", 
            "closed_issue",
        )
    )


class IssueAdmin(ModelAdmin):
    list_display = ["user", "utopic", "title"]
    list_display_links = list_display
    search_fields = ["title", "body"]
    list_filter = ["status", "created"]


site.register(Content, ContentAdmin)
site.register(Commit, CommitAdmin)
site.register(UTopic, UtopicAdmin)
site.register(Category)
site.register(SearchedWords, SearchedWordsAdmin)
site.register(ReportModel)
site.register(UserProfile, UserProfileAdmin)
site.register(Topic, TopicAdmin)
site.register(Issue, IssueAdmin)