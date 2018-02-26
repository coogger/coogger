#django
from django.http import *
from django.shortcuts import render
from django.contrib.auth import *
from django.contrib import messages
from django.db.models import F
from django.db.models import Q
from django.contrib import messages as ms

#django class based
from django.views.generic.base import TemplateView
from django.views import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

#form
from apps.cooggerapp.forms import ReportsForm

#models
from apps.cooggerapp.models import Content,OtherInformationOfUsers,Notification,SearchedWords,Following,Report

#views
from apps.cooggerapp.views.tools import paginator,hmanynotifications

class Home(TemplateView):
    template_name = "apps/cooggerapp/card/blogs.html"
    pagi = 20
    queryset = Content.objects.filter(confirmation = True)

    def get_context_data(self, **kwargs):
        context = super(Home, self).get_context_data(**kwargs)
        context["content"] = paginator(self.request,self.queryset,self.pagi)
        context["hmanynotifications"] = hmanynotifications(self.request)
        return context


class FollowingContent(View):
    template_name = "apps/cooggerapp/card/blogs.html"
    pagi = 16

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        oof = []
        queryset = []
        for i in Following.objects.filter(user = request.user):
            i_wuser = i.which_user
            oof.append(i.which_user)
        for q in Content.objects.filter(confirmation = True):
            if q.user in oof:
                queryset.append(q)
        info_of_cards = paginator(request,queryset,self.pagi)
        context = dict(
        content = info_of_cards,
        hmanynotifications = hmanynotifications(request),
        )
        return render(request, self.template_name, context)


class Search(TemplateView):
    template_name = "apps/cooggerapp/card/blogs.html"
    pagi = 20

    def get_context_data(self, **kwargs):
        context = super(Search, self).get_context_data(**kwargs)
        context["content"] = paginator(self.request,self.get_queryset(),self.pagi)
        return context

    def get_form_data(self,name = "query"):
        name = self.request.GET[name].lower()
        SearchedWords(word = name).save()
        return name

    def search_algorithm(self):
        searched_data = self.get_form_data()
        q = Q(title__contains = searched_data) | Q(content_list__contains = searched_data) | Q(content__contains = searched_data)
        queryset = Content.objects.filter(q,confirmation = True).order_by("-views")
        return queryset

    def get_queryset(self):
        queryset = self.search_algorithm()
        return queryset


class Notification(View):
    template_name = "apps/cooggerapp/home/notifications.html"
    pagi = 10

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        queryset = Notification.objects.filter(user = self.request.user).order_by("-time")
        context = dict(
        notifications = paginator(request,queryset,self.pagi),
        hmanynotifications = queryset.filter(show=False).count(),
        )
        queryset.update(show = True)
        return render(request, self.template_name, context)


class Report(View):
    form_class = ReportsForm
    initial = {'key': 'value'}
    template_name = "apps/cooggerapp/home/report.html"

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        report_form = self.form_class(initial = self.initial)
        context = dict(
        report_form = report_form,
        content_id = hmanynotifications(request),
        )
        return render(request, self.template_name, context)

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        report_form = self.form_class(request.POST)
        if report_form.is_valid():
            content = Content.objects.filter(id = request.POST["content_id"])[0]
            if Report.objects.filter(user = request_user,content = content).exists():
                ms.error(request,"Şikayetiniz değerlendirme sürecinde.")
                return HttpResponseRedirect("/")
            report_form  = report_form.save(commit=False)
            report_form.user = request.user
            report_form.content = content
            report_form.save()
            ms.error(request,"Şikayetiniz alınmıştır.")
            return HttpResponseRedirect("/")
        return HttpResponse(self.get(request, *args, **kwargs))
