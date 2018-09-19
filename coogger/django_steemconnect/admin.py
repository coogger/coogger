from django.http import Http404
from django.contrib.admin import site, ModelAdmin
from django.contrib.auth.models import User

# models
from django_steemconnect.models import SteemConnectUser, Community, Mods


class SteemConnectUserAdmin(ModelAdmin):
    list_display = ["user"]
    list_display_links = ["user"]
    search_fields = ["user"]


class ModsAdmin(ModelAdmin):
    list_display = ["community", "user"]
    list_display_links = ["community", "user"]
    search_fields = ["community", "user"]

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        community_model = self.get_community_model(request)
        return qs.filter(community = community_model)

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        if request.user.is_superuser:
            return form
        community_queryset = Community.objects.filter(name=self.get_community_model(request).name)
        form.base_fields["community"]._queryset = community_queryset
        return form

    def save_model(self, request, obj, form, change):
        if request.user.is_superuser or self.get_community_model(request) == obj.community:
            User.objects.filter(username=object.user.username).update(is_staff=True)
            super(ModsAdmin, self).save_model(request, obj, form, change)

    def delete_model(self, request, object):
        User.objects.filter(username=object.user.username).update(is_staff=False)
        object.delete()

    def get_community_model(self, request):
        return Mods.objects.filter(user = request.user)[0].community


class CommunityAdmin(ModelAdmin):
    list_display = ["name", "management"]
    list_filter = ["name"]
    list_display_links = ["name", "management"]
    search_fields = [
                        "name", "host_name", "redirect_url", "client_id",
                        "app_secret", "login_redirect", "scope", "management",
                        "ms", "icon_address"
                    ]
    fields = (
                ("management"),
                ("name", "host_name"),
                ("redirect_url", "client_id", "app_secret"),
                ("login_redirect", "scope"),
                ("icon_address", "ms","active"),
                ("definition", "image"),
             )

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        community_model = self.get_community_model(request)
        return qs.filter(name = community_model.name)

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        if request.user.is_superuser:
            return form
        if self.get_community_model(request) == obj:
            return form
        raise Http404

    def save_model(self, request, obj, form, change):
        if request.user.is_superuser or self.get_community_model(request) == obj:
            super(CommunityAdmin, self).save_model(request, obj, form, change)

    def get_community_model(self, request):
        return Mods.objects.filter(user = request.user)[0].community



site.register(SteemConnectUser, SteemConnectUserAdmin)
site.register(Community, CommunityAdmin)
site.register(Mods, ModsAdmin)
