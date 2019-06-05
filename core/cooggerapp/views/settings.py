# django
from django.shortcuts import render, redirect
from django.contrib import messages

# class
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin

# models
from ..models import UserProfile, OtherAddressesOfUsers

# forms
from ..forms import AddressesForm

# python
import os


class Settings(LoginRequiredMixin, View):
    template_name = "settings/settings.html"

    def get(self, request, *args, **kwargs):
        address = self.address(request)
        context = dict(
            # user_profile_form=
            address_form=address[1],
            address_instance=address[0],
        )
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
                messages.error(request, "Your website has added")

