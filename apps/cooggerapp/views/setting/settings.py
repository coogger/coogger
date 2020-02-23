from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect, render
from django.views import View
from django.views.generic import UpdateView

from ...forms import AddressesForm
from ...models import UserProfile


class UserSetMixin(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = User
    fields = ["first_name", "last_name", "email"]
    template_name = "settings/user.html"
    success_message = "Your settings updated"
    success_url = "/settings/user/"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(settings_list=["user", "extra", "address"])
        return context

    def get_object(self, queryset=None):
        return self.model.objects.get(username=self.request.user.username)


class Settings(UserSetMixin):
    pass


class UserExtra(UserSetMixin):
    model = UserProfile
    fields = ["bio", "about", "email_permission"]
    template_name = "settings/userextra.html"
    success_url = "/settings/extra/"

    def get_object(self):
        return self.model.objects.get(user=self.request.user)


class Address(LoginRequiredMixin, View):
    template_name = "settings/address.html"

    def get(self, request, *args, **kwargs):
        address = self.address(request)
        context = dict(
            # user_profile_form=
            address_form=address[1],
            address_instance=address[0],
        )
        context.update(settings_list=["user", "extra", "address"])
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        try:
            self.post_address(request)
        except Exception as e:
            messages.error(request, e)
        return redirect(request.META["PATH_INFO"])

    def address(self, request):
        address_instance = UserProfile.objects.get(user=request.user).address.all()
        address_form = AddressesForm(request.GET or None)
        return address_instance, address_form

    def post_address(self, request):
        form = AddressesForm(request.POST)
        if form.is_valid():
            form = form.save(commit=False)
            if form.choices is not None and form.address:
                form.save()
                UserProfile.objects.get(user=request.user).address.add(form)
                messages.success(request, "Your website has added")
