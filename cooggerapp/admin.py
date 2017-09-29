from django.contrib import admin
from cooggerapp.models import *
from django.utils import timezone
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from cooggerapp.models import Author

class BlogAdmin(admin.ModelAdmin):
    list_display = ["category","title","time"]
    list_display_links = ["category","title","time"]
    list_filter = ["category","time"]
    search_fields = ["category","title","tag","text"]
    prepopulated_fields = {"url":("title",)}
    fields = (("username","content_list"),("category","subcategory","category2"),("title","url"),"content","tag")

    class Media:
        js = ("js/my-admin-content.js",)


class AuthorAdmin(admin.StackedInline):
    model = Author
    can_delete = False
    verbose_name_plural = 'Yazar, iban'


class UserAdmin(BaseUserAdmin):
    #Mevcut modele(tasarıma) yeni özellikleri entegre ediyoruz. Bu bize admin panelde görünecektir.
    inlines = (AuthorAdmin, )


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(Blog,BlogAdmin)