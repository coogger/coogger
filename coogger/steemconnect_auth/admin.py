from django.http import Http404
from django.contrib.admin import site, ModelAdmin
from django.contrib.auth.models import User, Group

# models
from steemconnect_auth.models import SteemConnectUser, Community, Mods, CommunitySettings, CategoryofCommunity


class CommunitySettingsAdmin(ModelAdmin):
    list_ = ["community","beneficiaries"]
    list_display = list_
    list_display_links = list_
    search_fields = list_


class CategoryofCommunityAdmin(ModelAdmin):
    list_ = ["community","category_name"]
    list_display = list_
    list_display_links = list_
    search_fields = list_

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        community_model = Community.objects.filter(management=request.user)[0]
        categories = self.get_categories(request)
        qs = qs.filter(community=community_model, category_name__in=categories)
        return qs


    def get_form(self, request, obj=None, **kwargs):
        if request.user.is_superuser:
            return super().get_form(request, obj, **kwargs)
        community_model = Community.objects.filter(management=request.user)[0]
        form = super().get_form(request, obj, **kwargs)
        form.base_fields["community"].choices = ((community_model.id, community_model),)
        return form

    def get_categories(self, request):
        community_model = Community.objects.filter(management=request.user)[0]
        categories = [
            category.category_name for category in \
                CategoryofCommunity.objects.filter(community=community_model)
            ]
        return categories


class SteemConnectUserAdmin(ModelAdmin):
    list_display = ["user"]
    list_display_links = ["user"]
    search_fields = ["user"]


class ModsAdmin(ModelAdmin):
    "Just accept superuser and community manager"

    list_display = ["community", "user"]
    list_display_links = ["community", "user"]
    search_fields = ["community", "user"]

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        community_model = self.get_management_community(request)[0]
        return qs.filter(community = community_model)

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        if request.user.is_superuser:
            return form
        community_queryset = self.get_management_community(request)
        form.base_fields["community"]._queryset = community_queryset
        return form

    def save_model(self, request, obj, form, change):
        if request.user.is_superuser or self.get_management_community(request).exists():
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

    def get_management_community(self, request):
        return Community.objects.filter(management=request.user)


class CommunityAdmin(ModelAdmin):
    list_display = ["name", "management"]
    list_filter = ["name"]
    list_display_links = ["name", "management"]
    search_fields = ["name", "host_name","client_id","app_secret",]
    fields = (
                ("management", "beneficiaries"),
                ("name", "host_name"),
                ("redirect_url", "client_id"),
                ("login_redirect", "scope"),
                ("icon_address", "ms"),
                ("definition", "image"),
                ("app_secret", "active"),
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
site.register(CommunitySettings, CommunitySettingsAdmin)
site.register(CategoryofCommunity, CategoryofCommunityAdmin)
