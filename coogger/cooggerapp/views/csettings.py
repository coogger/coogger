#django
from django.http import *
from django.shortcuts import render
from django.contrib.auth import *
from django.contrib import messages as ms
from django.contrib.auth.models import User

# class
from django.views import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic.base import TemplateView

#models
from cooggerapp.models import UserFollow, OtherInformationOfUsers, Content

#views
from cooggerapp.views.tools import paginator,get_community_model

#forms
from cooggerapp.forms import CSettingsUserForm,UserFollowForm,CooggerupForm,VotepercentForm,BeneficiariesForm

#python
import os

class Settings(View):
    template_name = "settings/settings.html"

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        address = self.address(request)
        community_model = get_community_model(request)
        context = dict(
        community = community_model,
        address_form = address[1],
        address_instance = address[0],
        cooggerup_form = self.cooggerup(request),
        vote_percent_form = self.vote_percent(request),
        beneficiaries_percent_form = self.beneficiaries(request),
        )
        return render(request,self.template_name,context)

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        self.post_coogger_up(request)
        self.post_address(request)
        self.post_vote_percent(request)
        self.post_beneficiaries(request)
        return HttpResponseRedirect(request.META["PATH_INFO"])

    def address(self,request):
        address_instance = UserFollow.objects.filter(user = request.user)
        address_form = UserFollowForm(request.GET or None)
        return address_instance,address_form

    def post_address(self,request):
        form = UserFollowForm(request.POST)
        if form.is_valid():
            form = form.save(commit=False)
            if form.choices != None and form.adress != None:
                form.user = request.user
                form.save()
                ms.error(request,"Your website has added")

    def cooggerup(self,request):
        cooggerup_instance = OtherInformationOfUsers.objects.filter(user = request.user)[0]
        cooggerup_form = CooggerupForm(request.GET or None,instance = cooggerup_instance)
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
                otherinfo_filter = OtherInformationOfUsers.objects.filter(user = request.user)
                otherinfo_filter.update(cooggerup_confirmation = True,cooggerup_percent = int(percent))
                ms.error(request,"You joined in curation trails of the cooggerup bot")
            elif confirmation == "of":
                otherinfo_filter = OtherInformationOfUsers.objects.filter(user = request.user)
                otherinfo_filter.update(cooggerup_confirmation = False,cooggerup_percent = 0)
                ms.error(request,"You have been removed from the curation trails of cooggerup bot.")

    def vote_percent(self,request):
        vote_percent_instance = OtherInformationOfUsers.objects.filter(user = request.user)[0]
        vote_percent_form = VotepercentForm(request.GET or None,instance = vote_percent_instance)
        return vote_percent_form

    def post_vote_percent(self,request):
        form = VotepercentForm(request.POST)
        if form.is_valid():
            percent = request.POST["vote_percent"]
            otherinfo_filter = OtherInformationOfUsers.objects.filter(user = request.user)
            otherinfo_filter.update(vote_percent = int(percent))
            ms.error(request,"Your voting percentage is set")

    def beneficiaries(self,request):
        beneficiaries_percent_instance = OtherInformationOfUsers.objects.filter(user = request.user)[0]
        beneficiaries_percent_form = BeneficiariesForm(request.GET or None,instance = beneficiaries_percent_instance)
        return beneficiaries_percent_form

    def post_beneficiaries(self,request):
        form = BeneficiariesForm(request.POST)
        if form.is_valid():
            percent = request.POST["beneficiaries"]
            OtherInformationOfUsers.objects.filter(user = request.user).update(beneficiaries = int(percent))
            if percent != "0":
                ms.error(request,"Thank you for supporting Coogger")
