# django
from django.shortcuts import render
from django.contrib import messages

# class
from django.views import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

# models
from cooggerapp.models import OtherAddressesOfUsers, OtherInformationOfUsers

# forms
from cooggerapp.forms import (OtherAddressesOfUsersForm,
    CooggerupForm, VotepercentForm, BeneficiariesForm
)

# python
import os


class Settings(View):
    template_name = "settings/settings.html"

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        address = self.address(request)
        context = dict(
            address_form=address[1],
            address_instance=address[0],
            cooggerup_form=self.cooggerup(request),
            vote_percent_form=self.vote_percent(request),
            beneficiaries_percent_form=self.beneficiaries(request),
        )
        return render(request, self.template_name, context)

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        try:
            self.post_coogger_up(request)
            self.post_address(request)
            self.post_vote_percent(request)
            self.post_beneficiaries(request)
        except Exception as e:
            messages.error(request, e)
        return HttpResponseRedirect(request.META["PATH_INFO"])

    def address(self, request):
        address_instance = OtherAddressesOfUsers.objects.filter(user=request.user)
        address_form = OtherAddressesOfUsersForm(request.GET or None)
        return address_instance, address_form

    def post_address(self, request):
        form = OtherAddressesOfUsersForm(request.POST)
        if form.is_valid():
            form = form.save(commit=False)
            if form.choices != None and form.adress != None:
                form.user = request.user
                form.save()
                messages.error(request, "Your website has added")

    def cooggerup(self, request):
        cooggerup_instance = OtherInformationOfUsers.objects.filter(user=request.user)[0]
        cooggerup_form = CooggerupForm(request.GET or None, instance=cooggerup_instance)
        return cooggerup_form

    def post_coogger_up(self, request):
        form = CooggerupForm(request.POST)
        if form.is_valid():
            try:
                confirmation = request.POST["cooggerup_confirmation"]
            except:
                confirmation = "of"
            percent = request.POST["cooggerup_percent"]
            if confirmation == "on":
                otherinfo_filter = OtherInformationOfUsers.objects.filter(user=request.user)
                if otherinfo_filter[0].cooggerup_percent != percent:
                    otherinfo_filter.update(cooggerup_confirmation=True, cooggerup_percent=float(percent))
                    messages.error(request, "You joined in curation trails of the cooggerup bot")
            elif confirmation == "of":
                otherinfo_filter = OtherInformationOfUsers.objects.filter(user=request.user)
                if otherinfo_filter[0].cooggerup_percent != 0:
                    otherinfo_filter.update(cooggerup_confirmation=False, cooggerup_percent=0)
                    messages.error(request, "You have been removed from the curation trails of cooggerup bot.")

    def vote_percent(self, request):
        vote_percent_instance = OtherInformationOfUsers.objects.filter(user=request.user)[0]
        vote_percent_form = VotepercentForm(request.GET or None, instance=vote_percent_instance)
        return vote_percent_form

    def post_vote_percent(self, request):
        form = VotepercentForm(request.POST)
        if form.is_valid():
            otherinfo_filter = OtherInformationOfUsers.objects.filter(user=request.user)
            percent = request.POST["vote_percent"]
            if otherinfo_filter[0].vote_percent != percent:
                otherinfo_filter.update(vote_percent=float(percent))
                messages.error(request, "Your voting percentage is set")

    def beneficiaries(self, request):
        beneficiaries_percent_instance = OtherInformationOfUsers.objects.filter(user=request.user)[0]
        beneficiaries_percent_form = BeneficiariesForm(request.GET or None, instance=beneficiaries_percent_instance)
        return beneficiaries_percent_form

    def post_beneficiaries(self, request):
        form = BeneficiariesForm(request.POST)
        if form.is_valid():
            otherinfoofusers = OtherInformationOfUsers.objects.filter(user=request.user)
            percent = request.POST["beneficiaries"]
            if otherinfoofusers[0].beneficiaries != percent:
                otherinfoofusers.update(beneficiaries=int(percent))
                if percent != "0":
                    messages.error(request, "Thank you for supporting Coogger ecosystem")
