from django.contrib.admin import ModelAdmin, StackedInline, site, TabularInline, AdminSite
from django.utils import timezone
from django.contrib import messages as ms
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from django.http import Http404

#models
from cooggerapp.models import Content, Contentviews, UserFollow, SearchedWords, ReportModel, OtherInformationOfUsers
from django_steemconnect.models import Mods

# forms
from cooggerapp.forms import ContentForm

#choices
from cooggerapp.choices import *

# python
import datetime


class ContentAdmin(ModelAdmin):
    list_ = ["community_name","user","permlink",
            "mod","cooggerup","status"]
    list_display = list_
    list_display_links = list_
    list_filter = ["status","time","cooggerup"]
    search_fields = ["topic","title"]
    fields = (("user","title"),"content","tag",("category","language","topic"),("status","cooggerup"))

    class Media:
        css = {
        'coogger.css': ('https://cdn.rawgit.com/hakancelik96/63242e5ebb5f64bea570d8c1b476004c/raw/f640a21a48429c2e2e32478853469a517906e7b7/coogger.css',),
        }

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        community = self.get_comminity_model(request)
        return qs.filter(community = community)

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        form.base_fields["category"].choices = make_choices(eval(str(obj.community.name)+"_categories()"))
        return form

    def save_model(self, request, obj, form, change):
        obj.lastmod = datetime.datetime.now()
        obj.mod = request.user
        super(ContentAdmin, self).save_model(request, obj, form, change)

    def get_comminity_model(self, request):
        return Mods.objects.filter(user = request.user)[0].community


class UserFollowAdmin(ModelAdmin):
    list_ = ["user","choices","adress"]
    list_display = list_
    list_display_links = list_
    list_filter = ["choices"]
    search_fields = list_

    def save_model(self, request, obj, form, change):
        if request.user.is_superuser:
            super(UserFollowAdmin, self).save_model(request, obj, form, change)
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
    list_ = ["user","cooggerup_confirmation","cooggerup_percent"]
    list_display = list_
    list_display_links = list_
    search_fields = list_
    list_filter = ["cooggerup_confirmation"]

    def save_model(self, request, obj, form, change):
        if request.user.is_superuser:
            super(OtherInfoUsersAdmin, self).save_model(request, obj, form, change)
        raise Http404


site.register(Content,ContentAdmin)
site.register(Contentviews,ContentviewsAdmin)
site.register(UserFollow,UserFollowAdmin)
site.register(SearchedWords,SearchedWordsAdmin)
site.register(ReportModel)
site.register(OtherInformationOfUsers,OtherInfoUsersAdmin)
