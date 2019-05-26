# django
from django.shortcuts import render, redirect
from django.contrib import messages

# class
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin

# models
from core.cooggerapp.models import OtherAddressesOfUsers, OtherInformationOfUsers

# forms
from core.cooggerapp.forms import OtherAddressesOfUsersForm

# python
import os


class Settings(LoginRequiredMixin, View):
    template_name = "settings/settings.html"

    def get(self, request, *args, **kwargs):
        address = self.address(request)
        context = dict(
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
        address_instance = OtherAddressesOfUsers.objects.filter(user=request.user)
        address_form = OtherAddressesOfUsersForm(request.GET or None)
        return address_instance, address_form

    def post_address(self, request):
        form = OtherAddressesOfUsersForm(request.POST)
        if form.is_valid():
            form = form.save(commit=False)
            if form.choices != None and form.address != None:
                form.user = request.user
                form.save()
                messages.error(request, "Your website has added")

