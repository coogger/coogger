# django
from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.generic.base import TemplateView
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import UpdateView
from django.urls import reverse
from django.contrib.auth.models import User

# models
from ..models import UserProfile, OtherAddressesOfUsers

# forms
from ..forms import AddressesForm

# python
import os

class User(LoginRequiredMixin, UpdateView):
    model = User
    fields = ["first_name", "last_name", "email"]
    template_name  = "settings/user.html"
    success_url = "/settings/user/"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context["settings_list"] = [
            "user",
            "user-extra",
            "address"
        ]
        return context
    
    def get_object(self):
        return self.model.objects.get(username=self.request.user.username)


class Settings(User):
    pass


class UserExtra(User):
    model = UserProfile
    fields = ["description", "about", "email_permission"]
    template_name  = "settings/userextra.html"
    success_url = "/settings/user-extra/"
    
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
        context["settings_list"] = [
            "user",
            "user-extra",
            "address"
        ]
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
            if form.choices != None and form.address != None:
                form.save()
                UserProfile.objects.get(user=request.user).address.add(form)
                messages.success(request, "Your website has added")

