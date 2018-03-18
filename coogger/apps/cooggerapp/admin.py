from django.contrib.admin import ModelAdmin,StackedInline,site,TabularInline,AdminSite
from django.utils import timezone
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from apps.cooggerapp.models import *

# python
import datetime

class ContentAdmin(ModelAdmin):
    list_ = ["user","content_list","title","dor","time","lastmod","views"]
    list_display = list_
    list_display_links = list_
    list_filter = ["time","confirmation"]
    search_fields = list_
    prepopulated_fields = {"url":("title",)}
    fields = ("user","confirmation",("content_list"),("title","url"),"content","show","tag",("views","hmanycomment","dor"))

    def save_model(self, request, obj, form, change):
        # admin panelde her düzenleme yapıldıgında 1 artmasın istiyorsan
        # confirmation'ı true yapmadan düzenlemen gerek.
        obj.lastmod = datetime.datetime.now()
        oiouof = OtherInformationOfUsers.objects.filter(user = request.POST["user"])
        if obj.confirmation == True:
            oiouof.update(hmanycontent = F("hmanycontent") + 1)
        elif obj.confirmation == False:
            oiouof.update(hmanycontent = F("hmanycontent") - 1)
        super(ContentAdmin, self).save_model(request, obj, form, change)

class NotificationAdmin(ModelAdmin):
    list_ = ["user","even","content","show","address","time"]
    list_display = list_
    list_display_links = list_
    search_fields = list_

class UserFollowAdmin(ModelAdmin):
    list_ = ["user","choices","adress"]
    list_display = list_
    list_display_links = list_
    list_filter = ["choices"]
    search_fields = list_

class CommentAdmin(ModelAdmin):
    list_ = ["user","content_id","comment"]
    list_display = list_
    list_display_links = list_
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

## users ##
class OtherInformationOfUsersAdmin(StackedInline):
    model = OtherInformationOfUsers
    can_delete = False
    verbose_name_plural = 'kullanıcıların diğer bilgileri'


class UserAdmin(UserAdmin):
    inlines = (OtherInformationOfUsersAdmin, )

site.unregister(User)

site.register(User, UserAdmin)

site.register(Content,ContentAdmin)

site.register(Comment,CommentAdmin)

site.register(Contentviews,ContentviewsAdmin)

site.register(UserFollow,UserFollowAdmin)

site.register(SearchedWords,SearchedWordsAdmin)

site.register(Notification,NotificationAdmin)

site.register(Report)
