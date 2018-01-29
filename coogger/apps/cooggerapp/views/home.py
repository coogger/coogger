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

class HomeBasedClass(TemplateView):
    template_name = "card/blogs.html"
    pagi = 20
    queryset = Content.objects.filter(confirmation = True)

    def get_context_data(self, **kwargs):
        context = super(HomeBasedClass, self).get_context_data(**kwargs)
        context["content"] = paginator(self.request,self.queryset,self.pagi)
        context["hmanynotifications"] = hmanynotifications(self.request)
        return context


class FollowingContentBasedClass(View):
    template_name = "card/blogs.html"
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


class SearchBasedClass(TemplateView):
    template_name = "card/blogs.html"
    pagi = 20

    def get_context_data(self, **kwargs):
        query = self.request.GET["query"].lower()
        q = Q(title__contains = query) | Q(content_list__contains = query) | Q(tag__contains = query)
        queryset = Content.objects.filter(q,confirmation = True).order_by("-views")
        info_of_cards = paginator(self.request,queryset,self.pagi)
        data_search = SearchedWords.objects.filter(word = query)
        if data_search.exists():
            data_search = data_search[0]
            data_search.hmany = F("hmany") + 1
            data_search.save()
        else:
            SearchedWords(word = query).save()
        context = super(SearchBasedClass, self).get_context_data(**kwargs)
        context["content"] = info_of_cards
        return context


class NotificationBasedClass(View):
    template_name = "home/notifications.html"
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


class ReportBasedClass(View):
    form_class = ReportsForm
    initial = {'key': 'value'}
    template_name = "home/report.html"

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
