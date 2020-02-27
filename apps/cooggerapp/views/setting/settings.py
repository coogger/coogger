from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect, render
from django.views import View
from django.views.generic import UpdateView, FormView

from ...forms import AddressesForm
from ...models import UserProfile


class SettingMixin(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = User
    fields = ["first_name", "last_name", "email"]
    template_name = "settings/user.html"
    success_message = "Your settings updated"
    success_url = "/settings/user/"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["settings_list"] = ["user", "extra", "address"]
        return context

    def get_object(self):
        return self.model.objects.get(username=self.request.user.username)


class Settings(SettingMixin):
    pass


class UserExtra(SettingMixin):
    model = UserProfile
    fields = ["bio", "about", "email_permission"]
    template_name = "settings/userextra.html"
    success_url = "/settings/extra/"

    def get_object(self):
        return self.model.objects.get(user=self.request.user)


class Address(LoginRequiredMixin, SuccessMessageMixin, FormView):
    template_name = "settings/address.html"
    form_class = AddressesForm
    success_message = "Your settings updated"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["address_instance"] = UserProfile.objects.get(user=self.request.user).address.all()
        context["settings_list"] = ["user", "extra", "address"]
        return context

    def form_valid(self, form):
        UserProfile.objects.get(user=self.request.user).address.add(form.save())
        return super().form_valid(form)

    def get_success_url(self):
        return self.request.META["PATH_INFO"]
