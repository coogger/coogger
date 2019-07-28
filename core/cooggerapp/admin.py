from django.contrib import admin

#models
from core.cooggerapp.models import (
    Content,
    SearchedWords,
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


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass


@admin.register(Content)
class ContentAdmin(admin.ModelAdmin):
    list_display = ["user","permlink","reply"]
    list_display_links = list_display
    list_filter = ["status"]
    search_fields = ["user__username", "permlink", "title", "body"]
    prepopulated_fields = {"permlink": ("title",)}
    fields = (
        ("user"),
        ("category", "language", "utopic"),
        ("title", "permlink"),
        ("reply"),
        ("body"),
        ("tags", "status"),
        ("reply_count"),
    )


@admin.register(SearchedWords)
class SearchedWordsAdmin(admin.ModelAdmin):
    list_display = ["word","hmany"]
    list_display_links = list_display
    search_fields = list_display


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ["user"]
    list_display_links = list_display
    filter_horizontal = ("address", )
    search_fields = ["user__username"]


@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    list_ = ["name", "tags", "editable"]
    list_display = list_
    list_display_links = list_
    list_filter = ["editable"]
    search_fields = ["name","definition"]
    fields = (
        ("name", "permlink"),
        ("tags"),
        ("definition"),
        ("image_address"),
        ("address"),
        ("editable"),
    )


@admin.register(Commit)
class CommitAdmin(admin.ModelAdmin):
    list_display = ["content", "utopic"]
    list_display_links = ["content", "utopic"]
    list_filter = ["created"]
    search_fields = ["user__username", "utopic__name", "msg"]


@admin.register(UTopic)
class UtopicAdmin(admin.ModelAdmin):
    list_display = ["user", "name"]
    list_display_links = ["user", "name"]
    search_fields = ["user__username", "name"]
    fields = (
        ("user"),
        ("name", "permlink"),
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


@admin.register(Issue)
class IssueAdmin(admin.ModelAdmin):
    list_display = ["user", "utopic", "title"]
    list_display_links = list_display
    search_fields = ["user__username", "utopic__name", "title"]
    list_filter = ["status", "created"]
