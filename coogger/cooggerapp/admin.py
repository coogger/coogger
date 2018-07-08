from django.contrib.admin import ModelAdmin,StackedInline,site,TabularInline,AdminSite
from django.utils import timezone
from django.contrib import messages as ms
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin

#models
from cooggerapp.models import *

# python
import datetime

class CommunityAdmin(ModelAdmin):
    list_ = ["name","host_name","redirect_url","client_id","app_secret","login_redirect","scope","icon_address","ms"]
    list_display = list_
    list_display_links = list_
    list_filter = list_
    search_fields = list_
    fields = list_

class ContentAdmin(ModelAdmin):
    list_ = ["user","topic","permlink","mod","cooggerup","status","time"]
    list_display = list_
    list_display_links = list_
    list_filter = ["status","time","cooggerup"]
    search_fields = ["topic","title"]
    fields = ("user","title","content","tag",("right_side","left_side","topic"),("status"))

    def save_model(self, request, obj, form, change):
        obj.lastmod = datetime.datetime.now()
        obj.mod = request.user
        oiouof = OtherInformationOfUsers.objects.filter(user = request.POST["user"])
        content_count = Content.objects.filter(user = obj.user,status = "approved").count()
        oiouof.update(hmanycontent = content_count)
        super(ContentAdmin, self).save_model(request, obj, form, change)

class UserFollowAdmin(ModelAdmin):
    list_ = ["user","choices","adress"]
    list_display = list_
    list_display_links = list_
    list_filter = ["choices"]
    search_fields = list_

class SearchedWordsAdmin(ModelAdmin):
    list_ = ["word","hmany"]
    list_display = list_
    list_display_links = list_
    search_fields = list_

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


site.register(Community,CommunityAdmin)
site.register(Content,ContentAdmin)
site.register(Contentviews,ContentviewsAdmin)
site.register(UserFollow,UserFollowAdmin)
site.register(SearchedWords,SearchedWordsAdmin)
site.register(ReportModel)
site.register(OtherInformationOfUsers,OtherInfoUsersAdmin)
