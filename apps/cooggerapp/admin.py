from django.contrib import admin

from apps.cooggerapp.models import (
    Commit,
    Content,
    Issue,
    ReportModel,
    SearchedWords,
    Topic,
    UserProfile,
    UTopic,
)

user_search_fields = ["user__username", "user__first_name", "user__last_name"]


@admin.register(ReportModel)
class ReportModelAdmin(admin.ModelAdmin):
    pass


@admin.register(Content)
class ContentAdmin(admin.ModelAdmin):
    list_display = ["user", "permlink"]
    list_display_links = list_display
    list_filter = ["status"]
    search_fields = ["permlink", "title", "body"] + user_search_fields
    prepopulated_fields = {"permlink": ("title",)}
    filter_horizontal = ("contributors",)


@admin.register(SearchedWords)
class SearchedWordsAdmin(admin.ModelAdmin):
    list_display = ["word", "hmany"]
    list_display_links = list_display
    search_fields = list_display


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ["user"]
    list_display_links = list_display
    filter_horizontal = ("address",)
    search_fields = user_search_fields
    fields = ["user", "bio", "address", "email_permission", "title"]


@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    list_ = ["name", "tags", "editable"]
    list_display = list_
    list_display_links = list_
    list_filter = ["editable"]
    search_fields = ["name", "description"]


@admin.register(Commit)
class CommitAdmin(admin.ModelAdmin):
    list_display = ["content", "utopic"]
    list_display_links = ["content", "utopic"]
    list_filter = ["created"]
    search_fields = ["utopic__name", "msg"] + user_search_fields


@admin.register(UTopic)
class UtopicAdmin(admin.ModelAdmin):
    list_display = ["user", "name"]
    list_display_links = ["user", "name"]
    search_fields = ["name"] + user_search_fields
    filter_horizontal = ("contributors",)


@admin.register(Issue)
class IssueAdmin(admin.ModelAdmin):
    list_display = ["user", "utopic", "title"]
    list_display_links = list_display
    search_fields = ["utopic__name", "title"] + user_search_fields
    list_filter = ["status", "created"]
