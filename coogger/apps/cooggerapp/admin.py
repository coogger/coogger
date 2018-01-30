from django.contrib.admin import ModelAdmin,StackedInline,site,TabularInline,AdminSite
from django.utils import timezone
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from apps.cooggerapp.models import *

class ContentAdmin(ModelAdmin):
    list_ = ["user","content_list","title","dor","time","lastmod","views"]
    list_display = list_
    list_display_links = list_
    list_filter = ["time","confirmation"]
    search_fields = list_
    prepopulated_fields = {"url":("title",)}
    fields = ("user","confirmation",("content_list"),("title","url"),"content","show","tag",("views","hmanycomment","dor"))


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
    list_filter = ["user"]
    search_fields = list_

class SearchedWordsAdmin(ModelAdmin):
    list_ = ["word","hmany"]
    list_display = list_
    list_display_links = list_
    search_fields = list_

## users ##
class OtherInformationOfUsersAdmin(StackedInline):
    model = OtherInformationOfUsers
    can_delete = False
    verbose_name_plural = 'kullanıcıların diğer bilgileri'
    list_filter = ["author","is_author"]

class OtherInformationOfUsersADMIN(ModelAdmin):
    list_ = ["user","author","is_author","pp","about","following","followers"]
    list_display = ["user","author","is_author","pp","following","followers"]
    list_display_links = ["user","author","is_author","pp","following","followers"]
    list_filter = list_
    search_fields = list_

class AuthorAdmin(StackedInline):
    model = Author
    can_delete = False
    verbose_name_plural = 'yazarlık bilgileri'

class UserAdmin(UserAdmin):
    inlines = (OtherInformationOfUsersAdmin,AuthorAdmin, )

site.unregister(User)

site.register(User, UserAdmin)

site.register(OtherInformationOfUsers,OtherInformationOfUsersADMIN)

site.register(Content,ContentAdmin)

site.register(Comment,CommentAdmin)

site.register(UserFollow,UserFollowAdmin)

site.register(SearchedWords,SearchedWordsAdmin)

site.register(Notification,NotificationAdmin)

site.register(Following)

site.register(Report)
