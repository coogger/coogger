from django.contrib.admin import ModelAdmin, site

#models
from core.cooggerapp.models import (
    Content, 
    Contentviews, 
    OtherAddressesOfUsers, 
    SearchedWords,
    ReportModel, 
    OtherInformationOfUsers, 
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
    list_display = ["user","permlink", "mod"]
    list_display_links = list_display
    list_filter = ["status", "cooggerup"]
    search_fields = ["title", "body", "permlink"]
    fields = (
        ("category"),
        ("language"),
        ("topic"),
        ("title"),
        ("permlink"),
        ("definition"),
        ("body"),
        ("tags"),
        ("cooggerup"),
        ("status"),
    )

    class Media:
        css = {
            "coogger.css": ("https://rawcdn.githack.com/coogger/coogger.css/11712e5084216bc25091db34e8796459736e2ae4/styles/coogger.css",),
        }

    def save_model(self, request, obj, form, change):
        obj.mod = request.user
        super().save_model(request, obj, form, change)


class OtherAddressesOfUsersAdmin(ModelAdmin):
    list_display = ["user", "choices", "address"]
    list_display_links = list_display
    list_filter = ["choices"]
    search_fields = ["choices", "address"]


class SearchedWordsAdmin(ModelAdmin):
    list_display = ["word","hmany"]
    list_display_links = list_display
    search_fields = list_display


class ContentviewsAdmin(ModelAdmin):
    list_ = ["content","ip"]
    list_display = list_
    list_display_links = list_
    search_fields = list_


class OtherInformationOfUsersAdmin(ModelAdmin):
    list_display = ["user"]
    list_display_links = list_display
    

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

    class Media:
        css = {
            "coogger.css": ("https://rawcdn.githack.com/coogger/coogger.css/11712e5084216bc25091db34e8796459736e2ae4/styles/coogger.css",),
        }


class CommitAdmin(ModelAdmin):
    list_display = ["content", "utopic"]
    list_display_links = ["content", "utopic"]
    list_filter = ["created"]
    search_fields = ["msg"]
    fields = (
        ("hash"),
        ("body"),
        ("msg"),
        ("created"),
    )

    class Media:
        css = {
            "coogger.css": ("https://rawcdn.githack.com/coogger/coogger.css/11712e5084216bc25091db34e8796459736e2ae4/styles/coogger.css",),
        }


class UtopicAdmin(ModelAdmin):
    list_display = ["user", "name"]
    list_display_links = ["user", "name"]
    search_fields = ["name"]
    fields = (
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
    fields = (
        ("user"),
        ("utopic"),
        ("permlink"),
        ("title"),
        ("body"),
        (
            "reply", 
            "status", 
            "reply_count", 
            "issue_id",
            "created",
        )
    )


site.register(Content, ContentAdmin)
site.register(Commit, CommitAdmin)
site.register(UTopic, UtopicAdmin)
site.register(Category)
site.register(Contentviews, ContentviewsAdmin)
site.register(OtherAddressesOfUsers, OtherAddressesOfUsersAdmin)
site.register(SearchedWords, SearchedWordsAdmin)
site.register(ReportModel)
site.register(OtherInformationOfUsers, OtherInformationOfUsersAdmin)
site.register(Topic, TopicAdmin)
site.register(Issue, IssueAdmin)