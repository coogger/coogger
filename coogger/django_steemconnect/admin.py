from django.http import Http404
from django.contrib.admin import site, ModelAdmin
from django.contrib.auth.models import User, Group

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
        community_model = request.community_model
        return qs.filter(community = community_model)

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        if request.user.is_superuser:
            return form
        community_queryset = Community.objects.filter(name=request.community_model.name)
        form.base_fields["community"]._queryset = community_queryset
        return form

    def save_model(self, request, obj, form, change):
        if request.user.is_superuser or request.community_model.management == request.user:
            if not obj.user.is_staff:
                management_user = User.objects.filter(username=obj.user).update(is_staff=True)
            if not obj.user.groups.filter(name="mod").exists():
                group = Group.objects.get(name="mod")
                obj.user.groups.add(group)
            super(ModsAdmin, self).save_model(request, obj, form, change)

    def delete_model(self, request, object):
        User.objects.filter(username=object.user.username).update(is_staff=False)
        object.delete()
        group = Group.objects.get(name="mod")
        object.user.groups.remove(group)


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
        community_model = request.community_model
        if community_model.management == request.user:
            return qs.filter(name = community_model.name)

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        if request.user.is_superuser:
            return form
        if request.community_model == obj:
            return form

    def save_model(self, request, obj, form, change):
        if request.user.is_superuser or request.community_model == obj:
            if not obj.management.is_staff:
                management_user = User.objects.filter(username=obj.management).update(is_staff=True)
            if not obj.management.groups.filter(name="community manager").exists():
                group = Group.objects.get(name='community manager')
                obj.management.groups.add(group)
            super(CommunityAdmin, self).save_model(request, obj, form, change)


site.register(SteemConnectUser, SteemConnectUserAdmin)
site.register(Community, CommunityAdmin)
site.register(Mods, ModsAdmin)
