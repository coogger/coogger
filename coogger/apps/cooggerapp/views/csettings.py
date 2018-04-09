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
from apps.cooggerapp.models import UserFollow, OtherInformationOfUsers, Content

#views
from apps.cooggerapp.views.tools import paginator

#forms
from apps.cooggerapp.forms import CSettingsUserForm,UserFollowForm,CooggerupForm

#python
import os

class Cooggerup(View):
    template_name = "apps/cooggerapp/settings/cooggerup.html"
    form_class = CooggerupForm

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        queryset = OtherInformationOfUsers.objects.filter(user = request.user)[0]
        context = dict(
        form = self.form_class(request.GET or None,instance = queryset),
        )
        return render(request, self.template_name, context)

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        bot_form = self.form_class(request.POST)
        if bot_form.is_valid():
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
            return HttpResponseRedirect(request.META["PATH_INFO"])


class Draft(TemplateView):
    template_name = "apps/cooggerapp/settings/draft.html"
    pagi = 6
    queryset = Content.objects.filter(draft = True)

    def get_context_data(self, **kwargs):
        context = super(Draft, self).get_context_data(**kwargs)
        context["content"] = paginator(self.request,self.queryset,self.pagi)
        return context


class Addaddess(View):
    form_class = UserFollowForm
    model = UserFollow
    template_name = "apps/cooggerapp/settings/add-address.html"

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        instance_ = self.model.objects.filter(user = request.user)
        user_form = self.form_class(request.GET or None)
        context = dict(
        UserForm = user_form,
        instance_ = instance_,
        )
        return render(request,self.template_name,context)

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        user_form = self.form_class(request.POST)
        if user_form.is_valid():
            form = user_form.save(commit=False)
            form.user = request.user
            form.save()
            ms.error(request,"Your website has added")
            return HttpResponseRedirect(request.META["PATH_INFO"])
