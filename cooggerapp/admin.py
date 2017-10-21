from django.contrib import admin
from cooggerapp.models import *
from django.utils import timezone
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from cooggerapp.models import OtherInformationOfUsers ,Views

class BlogAdmin(admin.ModelAdmin):
    list_ = ["username","content_list","title","category","dor","stars","hmstars","time","views"]
    list_display = list_
    list_display_links = list_
    list_filter = ["username","content_list","views","hmstars","dor","time"]
    search_fields = list_
    prepopulated_fields = {"url":("title",)}
    fields = (("username","content_list"),("category","subcategory","category2"),("title","url"),"content","tag")

    class Media:
        js = ("js/my-admin-content.js",)

class ViewsAdmin(admin.ModelAdmin):
    list_ = ["blog_id","ip"]
    list_display = list_
    list_display_links = list_
    search_fields = list_

class ContentListAdmin(admin.ModelAdmin):
    list_ = ["username","content_list","content_count"]
    list_display = list_
    list_display_links = list_
    list_filter = ["content_count"]
    search_fields = list_

class VotersAdmin(admin.ModelAdmin):
    list_ = ["username_id","blog_id","star"]
    list_display = list_
    list_display_links = list_
    list_filter = ["star"]
    search_fields = list_

class UserFollowAdmin(admin.ModelAdmin):
    list_ = ["user","choices","adress"]
    list_display = list_
    list_display_links = list_
    list_filter = ["choices"]
    search_fields = list_


## users ##
class OtherInformationOfUsersAdmin(admin.StackedInline):
    model = OtherInformationOfUsers
    can_delete = False
    verbose_name_plural = 'kullanıcıların diğer bilgileri'
    list_filter = ["author","is_author"]

class OtherInformationOfUsersADMIN(admin.ModelAdmin):
    list_ = ["author","is_author","pp"]
    list_display = list_
    list_display_links = list_
    list_filter = list_
    search_fields = list_


class AuthorAdmin(admin.StackedInline):
    model = Author
    can_delete = False
    verbose_name_plural = 'yazarlık bilgileri'


class UserAdmin(BaseUserAdmin):
    #Mevcut modele(tasarıma) yeni özellikleri entegre ediyoruz. Bu bize admin panelde görünecektir.
    inlines = (OtherInformationOfUsersAdmin,AuthorAdmin, )



admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(Views,ViewsAdmin)
admin.site.register(Blog,BlogAdmin)
admin.site.register(UserFollow,UserFollowAdmin)
admin.site.register(ContentList,ContentListAdmin)
admin.site.register(Voters,VotersAdmin)
admin.site.register(OtherInformationOfUsers,OtherInformationOfUsersADMIN)