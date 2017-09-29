from django.http import *
from django.shortcuts import render
from django.contrib.auth import *
from django.contrib import messages
from cooggerapp.models import *
from cooggerapp.views import tools

def main_detail(request,blog_path):
    "blogların detail kısmı "
    queryset = Blog.objects.filter(url = blog_path)[0]
    category = tools.Topics().category
    elastic_search = dict(
        title = "coogger | "+queryset.title,
        keywords =queryset.tag +",coogger "+str(queryset.username)+",coogger "+queryset.category+", "+queryset.title,
        description = "coogger "+str(queryset.username)+" "+queryset.category+" "+queryset.title
    )
    output = dict(
        detail = queryset,
        elastic_search = elastic_search,
        general = True,
        topics_category = category,
    )
    return render(request,"detail/main_detail.html",output)
