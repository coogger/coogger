from django.http import Http404
from django.contrib.admin import site, ModelAdmin
from django.contrib.auth.models import User, Group

# models
from steemconnect_auth.models import SteemConnectUser, Dapp, Mods, DappSettings, CategoryofDapp


class DappSettingsAdmin(ModelAdmin):
    list_ = ["dapp","beneficiaries"]
    list_display = list_
    list_display_links = list_
    search_fields = ["beneficiaries"]


class CategoryofDappAdmin(ModelAdmin):
    list_ = ["dapp","category_name"]
    list_display = list_
    list_display_links = list_
    search_fields = ["category_name"]

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        dapp_model = Dapp.objects.filter(management=request.user)[0]
        categories = self.get_categories(request)
        qs = qs.filter(dapp=dapp_model, category_name__in=categories)
        return qs


    def get_form(self, request, obj=None, **kwargs):
        if request.user.is_superuser:
            return super().get_form(request, obj, **kwargs)
        dapp_model = Dapp.objects.filter(management=request.user)[0]
        form = super().get_form(request, obj, **kwargs)
        form.base_fields["dapp"].choices = ((dapp_model.id, dapp_model),)
        return form

    def get_categories(self, request):
        dapp_model = Dapp.objects.filter(management=request.user)[0]
        categories = [
            category.category_name for category in \
                CategoryofDapp.objects.filter(dapp=dapp_model)
            ]
        return categories


class SteemConnectUserAdmin(ModelAdmin):
    list_display = ["user"]
    list_display_links = ["user"]


class ModsAdmin(ModelAdmin):
    "Just accept superuser and dapp manager"

    list_display = ["dapp", "user"]
    list_display_links = ["dapp", "user"]

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        dapp_model = self.get_management_dapp(request)[0]
        return qs.filter(dapp = dapp_model)

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        if request.user.is_superuser:
            return form
        dapp_queryset = self.get_management_dapp(request)
        form.base_fields["dapp"]._queryset = dapp_queryset
        return form

    def save_model(self, request, obj, form, change):
        if request.user.is_superuser or self.get_management_dapp(request).exists():
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

    def get_management_dapp(self, request):
        return Dapp.objects.filter(management=request.user)


class DappAdmin(ModelAdmin):
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
        dapp_model = request.dapp_model
        if dapp_model.management == request.user:
            return qs.filter(name = dapp_model.name)

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        if request.user.is_superuser:
            return form
        if request.dapp_model == obj:
            return form

    def save_model(self, request, obj, form, change):
        if request.user.is_superuser or request.dapp_model == obj:
            if not obj.management.is_staff:
                management_user = User.objects.filter(username=obj.management).update(is_staff=True)
            if not obj.management.groups.filter(name="dapp manager").exists():
                group = Group.objects.get(name='dapp manager')
                obj.management.groups.add(group)
            super(DappAdmin, self).save_model(request, obj, form, change)


site.register(SteemConnectUser, SteemConnectUserAdmin)
site.register(Dapp, DappAdmin)
site.register(Mods, ModsAdmin)
site.register(DappSettings, DappSettingsAdmin)
site.register(CategoryofDapp, CategoryofDappAdmin)
