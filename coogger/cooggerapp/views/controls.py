#django
from django.http import HttpResponseRedirect,HttpResponse
from django.shortcuts import render
from django.db.models import F
from django.contrib import messages as ms

# class
#from django.views.generic import ListView
from django.views import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

#models
from cooggerapp.models import Content,OtherInformationOfUsers

#form
from cooggerapp.forms import ContentForm

#python
import datetime


class Create(View):
    form_class = ContentForm
    template_name = "controls/create.html"

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        context = dict(
        create_form = self.form_class(),
        )
        return render(request, self.template_name, context)

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        request_user = request.user
        content_form = self.form_class(request.POST)
        if content_form.is_valid():
            content_form = content_form.save(commit = False)
            content_form.user = request_user
            save = content_form.content_save() # save with sc2py and get ms
            if save.status_code != 200: # if any error show the error
                ms.error(request,save.text)
            return HttpResponseRedirect("/"+content_form.get_absolute_url())
        else:
            context = dict(
            create_form = content_form,
            )
            ms.error(request, "unexpected error, check your content please or contact us on discord; <a gnrl='c-primary' href='https://discord.gg/q2rRY8Q'>https://discord.gg/q2rRY8Q</a>")
            return render(request, self.template_name, context)



class Change(View):
    form_class = ContentForm
    template_name = "controls/change.html"

    @method_decorator(login_required)
    def get(self, request, content_id, *args, **kwargs):
        request_user = request.user
        queryset = self.really_queryset(request,content_id)
        queryset = queryset[0]
        old_content_list = queryset.content_list
        content_form = self.form_class(instance=queryset)
        context = dict(
            change = queryset,
            content_id = content_id,
            change_form = content_form,
        )
        return render(request, self.template_name, context)

    @method_decorator(login_required)
    def post(self, request, content_id, *args, **kwargs):
        content_form = self.form_class(request.POST)
        if content_form.is_valid():
            content = content_form.save(commit=False)
            queryset = self.really_queryset(request,content_id)
            save = content.content_update(queryset,content) # save with sc2py and get ms
            if save.status_code != 200:
                ms.error(request,save.text)
            return HttpResponseRedirect("/"+content.get_absolute_url())

    @staticmethod
    def really_queryset(request,content_id):
        if request.user.is_superuser:
            queryset = Content.objects.filter(id = content_id)
        else:
            queryset = Content.objects.filter(user = request.user,id = content_id)
        return queryset
