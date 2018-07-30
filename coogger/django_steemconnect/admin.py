from django.contrib.admin import site,ModelAdmin

#models
from django_steemconnect.models import SteemConnectUser,Community,Mods

class SteemConnectUserAdmin(ModelAdmin):
    list_display = ["user"]
    list_display_links = ["user"]
    search_fields = ["user"]


class ModsAdmin(ModelAdmin):
    list_display = ["community","user"]
    list_display_links = ["community","user"]
    search_fields = ["community","user"]


class CommunityAdmin(ModelAdmin):
    list_display = ["name","management"]
    list_filter = ["name","management"]
    list_display_links = ["name","management"]
    search_fields = ["name","host_name","redirect_url","client_id","app_secret","login_redirect","scope","management","ms","icon_address"]
    fields = (("name","host_name"),("redirect_url","client_id","app_secret"),("login_redirect","scope"),"management","icon_address","ms")


site.register(SteemConnectUser, SteemConnectUserAdmin)
site.register(Community, CommunityAdmin)
site.register(Mods, ModsAdmin)
