#django
from django.http import HttpResponseRedirect,HttpResponse
from django.shortcuts import render
from django.db.models import F
from django.contrib import messages as ms
from django.contrib.sitemaps import Sitemap
from django.conf import settings

# class
from django.views.generic.base import TemplateView

# apps home
class AppsHome(TemplateView):
    template_name = "apps.html"

    def get_context_data(self, **kwargs):
        context = super(AppsHome, self).get_context_data(**kwargs)
        return context

# # apps sitemap
# class AppsSitemap(Sitemap):
#     changefreq = "weekly"
#     priority = 0.6
#
#     def items(self):
#         i_list = []
#         for i in settings.INSTALLED_APPS:
#             if i.startswith("apps."):
#                 i = i.split(".")
#                 if i[1] != "cooggerapp":
#                     url = i[0]+"/"+i[1]
#                     i_list.append(url)
#         return i_list
#
#     def location(self,obj):
#         return "/"+obj
