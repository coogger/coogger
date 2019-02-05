from django.http import Http404
from django.contrib.admin import site, ModelAdmin
from django.contrib.auth.models import User, Group

# models
from core.steemconnect_auth.models import SteemConnectUser, Dapp, CategoryofDapp


class CategoryofDappAdmin(ModelAdmin):
    list_ = ["dapp","name"]
    list_display = list_
    list_display_links = list_
    search_fields = ["name"]

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        dapp_model = Dapp.objects.filter(management=request.user)[0]
        categories = self.get_categories(request)
        qs = qs.filter(dapp=dapp_model, name__in=categories)
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
            category.name for category in \
                CategoryofDapp.objects.filter(dapp=dapp_model)
            ]
        return categories


class SteemConnectUserAdmin(ModelAdmin):
    list_display = ["user", "dapp"]
    list_display_links = ["user", "dapp"]


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
site.register(CategoryofDapp, CategoryofDappAdmin)
