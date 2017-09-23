from django.http import *
from django.shortcuts import render
from django.contrib.auth import *
from django.contrib import messages
from cooggerapp.models import *

def main_detail(request,blog_path):
    "blogların detail kısmı "
    queryset = Blog.objects.filter(url = blog_path)[0]
    elastic_search = dict(
        title = "coogger | "+queryset.title,
        keywords =queryset.tag +",coogger "+str(queryset.username)+",coogger "+queryset.category+", "+queryset.title,
        description = "coogger "+str(queryset.username)+" "+queryset.category+" "+queryset.title
    )
    output = dict(
        datail = queryset,
        elastic_search = elastic_search
    )
    return render(request,"detail/main_detail.html",output)
