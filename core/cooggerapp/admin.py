from django.contrib.admin import ModelAdmin, site
from django.http import Http404

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
    list_ = ["user","permlink", "mod"]
    list_display = list_
    list_display_links = list_
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
        if request.user.is_superuser:
            obj.mod = request.user
            super().save_model(request, obj, form, change)
        else:
            raise Http404


class OtherAddressesOfUsersAdmin(ModelAdmin):
    list_ = ["user","choices","address"]
    list_display = list_
    list_display_links = list_
    list_filter = ["choices"]
    search_fields = ["choices","address"]

    def save_model(self, request, obj, form, change):
        if request.user.is_superuser:
            super().save_model(request, obj, form, change)
        else:
            raise Http404


class SearchedWordsAdmin(ModelAdmin):
    list_ = ["word","hmany"]
    list_display = list_
    list_display_links = list_
    search_fields = list_

    def save_model(self, request, obj, form, change):
        if request.user.is_superuser:
            super().save_model(request, obj, form, change)
        else:
            raise Http404


class ContentviewsAdmin(ModelAdmin):
    list_ = ["content","ip"]
    list_display = list_
    list_display_links = list_
    search_fields = list_

    def save_model(self, request, obj, form, change):
        if request.user.is_superuser:
            super().save_model(request, obj, form, change)
        else:
            raise Http404 # mods or dapp leader cant change


class OtherInfoUsersAdmin(ModelAdmin):
    list_ = ["user", "cooggerup_confirmation", "cooggerup_percent", "sponsor", "beneficiaries"]
    list_display = list_
    list_display_links = list_
    search_fields = ["cooggerup_confirmation", "cooggerup_percent", "sponsor", "beneficiaries"]
    list_filter = ["cooggerup_confirmation", "cooggerup_percent", "sponsor", "beneficiaries"]

    def save_model(self, request, obj, form, change):
        if request.user.is_superuser:
            super().save_model(request, obj, form, change)
        else:
            raise Http404 # mods or dapp leader cant change


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


site.register(Content,ContentAdmin)
site.register(Commit, CommitAdmin)
site.register(UTopic, UtopicAdmin)
site.register(Category)
site.register(Contentviews,ContentviewsAdmin)
site.register(OtherAddressesOfUsers,OtherAddressesOfUsersAdmin)
site.register(SearchedWords,SearchedWordsAdmin)
site.register(ReportModel)
site.register(OtherInformationOfUsers,OtherInfoUsersAdmin)
site.register(Topic, TopicAdmin)
site.register(Issue)