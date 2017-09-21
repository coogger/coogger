from django.http import *
from django.shortcuts import render
from django.contrib.auth import *
from django.contrib import messages
from cooggerapp.models import *

def main_detail(request,blog_path):
    "blogların detail kısmı "
    queryset = Blog.objects.filter(url = blog_path)[0]
    output = dict(
        datail = queryset,
    )
    return render(request,"detail/main_detail.html",output)
