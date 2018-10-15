from django.contrib.admin import ModelAdmin, StackedInline, site, TabularInline, AdminSite
from django.utils import timezone
from django.contrib import messages as ms
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from django.http import Http404

#models
from cooggerapp.models import (Content, Contentviews, OtherAddressesOfUsers, SearchedWords,
    ReportModel, OtherInformationOfUsers)
from steemconnect_auth.models import Mods, Community

# forms
from cooggerapp.forms import ContentForm

#choices
from cooggerapp.choices import *

# python
import datetime


class ContentAdmin(ModelAdmin):
    list_ = ["community_name","user","permlink",
            "topic", "mod","cooggerup","status"]
    list_display = list_
    list_display_links = list_
    list_filter = ["status", "cooggerup"]
    search_fields = ["topic","title"]
    fields = (("user","title"),"content","tag",("category","language","topic"),("status","cooggerup"))

    class Media:
        css = {
        'coogger.css': ('https://cdn.rawgit.com/hakancelik96/63242e5ebb5f64bea570d8c1b476004c/raw/e9bc5b34abb95f612372f50d94b9ed209fd0a16b/coogger.css',),
        }

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        community_model = Community.objects.filter(management=request.user)[0]
        return qs.filter(community = community_model)

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        form.base_fields["category"].choices = request.categories
        return form

    def save_model(self, request, obj, form, change):
        obj.lastmod = datetime.datetime.now()
        obj.mod = request.user
        super(ContentAdmin, self).save_model(request, obj, form, change)


class OtherAddressesOfUsersAdmin(ModelAdmin):
    list_ = ["user","choices","address"]
    list_display = list_
    list_display_links = list_
    list_filter = ["choices"]
    search_fields = list_

    def save_model(self, request, obj, form, change):
        if request.user.is_superuser:
            super(OtherAddressesOfUsersAdmin, self).save_model(request, obj, form, change)
        raise Http404


class SearchedWordsAdmin(ModelAdmin):
    list_ = ["word","hmany"]
    list_display = list_
    list_display_links = list_
    search_fields = list_

    def save_model(self, request, obj, form, change):
        if request.user.is_superuser:
            super(SearchedWordsAdmin, self).save_model(request, obj, form, change)
        raise Http404


class ContentviewsAdmin(ModelAdmin):
    list_ = ["content_id","ip"]
    list_display = list_
    list_display_links = list_
    search_fields = list_


class OtherInfoUsersAdmin(ModelAdmin):
    list_ = ["user","cooggerup_confirmation","cooggerup_percent","sponsor", "beneficiaries"]
    list_display = list_
    list_display_links = list_
    search_fields = ["user"]
    list_filter = ["cooggerup_confirmation", "cooggerup_percent" ,"sponsor", "beneficiaries"]

    def save_model(self, request, obj, form, change):
        if request.user.is_superuser:
            super(OtherInfoUsersAdmin, self).save_model(request, obj, form, change)
        else:
            raise Http404 # mods or community leader cant change


site.register(Content,ContentAdmin)
site.register(Contentviews,ContentviewsAdmin)
site.register(OtherAddressesOfUsers,OtherAddressesOfUsersAdmin)
site.register(SearchedWords,SearchedWordsAdmin)
site.register(ReportModel)
site.register(OtherInformationOfUsers,OtherInfoUsersAdmin)
