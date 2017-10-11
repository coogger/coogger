from django.contrib import admin
from cooggerapp.models import *
from django.utils import timezone
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from cooggerapp.models import OtherInformationOfUsers

class BlogAdmin(admin.ModelAdmin):
    list_display = ["category","title","time"]
    list_display_links = ["category","title","time"]
    list_filter = ["time"]
    search_fields = ["title","tag"]
    prepopulated_fields = {"url":("title",)}
    fields = (("username","content_list"),("category","subcategory","category2"),("title","url"),"content","tag")

    class Media:
        js = ("js/my-admin-content.js",)


class ContentListAdmin(admin.ModelAdmin):
    list_display = ["username","content_list","content_count"]
    list_display_links = ["username","content_list","content_count"]
    list_filter = ["content_count"]
    search_fields = ["username","content_list","content_count"]

class VotersAdmin(admin.ModelAdmin):
    list_display = ["username_id","blog_id","star"]
    list_display_links = ["username_id","blog_id","star"]
    list_filter = ["star"]
    search_fields = ["username_id","blog_id","star"]

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
admin.site.register(Blog,BlogAdmin)
admin.site.register(ContentList,ContentListAdmin) 
admin.site.register(Voters,VotersAdmin) 
admin.site.register(OtherInformationOfUsers,OtherInformationOfUsersADMIN) 