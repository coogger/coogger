#django
from django.http import HttpResponseRedirect,HttpResponse
from django.shortcuts import render
from django.db.models import F
from django.contrib import messages as ms

# class
from django.views.generic.base import TemplateView

class Home(TemplateView):
    template_name = "apps/home.html"

    def get_context_data(self, **kwargs):
        context = super(Home, self).get_context_data(**kwargs)
        return context
