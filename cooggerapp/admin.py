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

## users ##
class OtherInformationOfUsersAdmin(admin.StackedInline):
    model = OtherInformationOfUsers
    can_delete = False
    verbose_name_plural = 'kullanıcıların diğer bilgileri'

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
