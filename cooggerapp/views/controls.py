#django
from django.http import HttpResponseRedirect,HttpResponse
from django.shortcuts import render
from django.db.models import F
from django.contrib import messages as ms

# class
from django.views.generic import ListView
from django.views import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

#models
from cooggerapp.models import Content,OtherInformationOfUsers

#views
from cooggerapp.views.tools import hmanynotifications,is_user_author

#form
from cooggerapp.forms import ContentForm

#python
import datetime

class CreateBasedClass(View):
    form_class = ContentForm
    template_name = "controls/create.html"

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        if is_user_author(request):
            context = dict(
            create_form = self.form_class(),
            hmanynotifications = hmanynotifications(request),
            )
            return render(request, self.template_name, context)

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        if is_user_author(request):
            request_user = request.user
            content_form = self.form_class(request.POST)
            if content_form.is_valid():
                content_form = content_form.save(commit=False)
                content_form.user = request_user
                content_form.confirmation = True
                OtherInformationOfUsers.objects.filter(user = request_user).update(hmanycontent = F("hmanycontent") + 1)
                content_form.save() # hiç hata olmaz ise kayıt etsindiye en sonda
                return HttpResponseRedirect("/"+content_form.url)
            return HttpResponse(self.get(request, *args, **kwargs))


class ChangeBasedClass(View):
    form_class = ContentForm
    template_name = "controls/change.html"

    @method_decorator(login_required)
    def get(self, request, content_id, *args, **kwargs):
        request_user = request.user
        if is_user_author(request):
            queryset = self.really_queryset(request,content_id)
            old_content_list = queryset.content_list
            content_form = self.form_class(instance=queryset)
            context = dict(
                change = queryset,
                content_id = content_id,
                change_form = content_form,
                hmanynotifications = hmanynotifications(request),
            )
            return render(request, self.template_name, context)

    @method_decorator(login_required)
    def post(self, request, content_id, *args, **kwargs):
        if is_user_author(request):
            content_form = self.form_class(request.POST)
            if content_form.is_valid():
                content = content_form.save(commit=False)
                queryset = self.really_queryset(request,content_id)
                content.user = queryset.user # içeriği yazan kişinin kullanıcı ismi
                content.time = queryset.time
                content.confirmation = True
                content.lastmod = datetime.datetime.now()
                content.save()
                return HttpResponseRedirect("/"+content.url)
            return HttpResponse(self.get(request,content_id, *args, **kwargs))

    @staticmethod
    def really_queryset(request,content_id):
        if request.user.is_superuser:
            queryset = Content.objects.filter(id = content_id)[0]
        else:
            queryset = Content.objects.filter(user = request.user,id = content_id)[0]
        return queryset
