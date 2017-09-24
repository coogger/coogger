from django.http import *
from django.shortcuts import render
from django.contrib.auth import *
from django.contrib import messages
from django.db.models import F
from cooggerapp.models import *
from cooggerapp.forms import *
from cooggerapp.blog_topics import *
from cooggerapp.views import tools

def home(request):
    queryset = Blog.objects.all()
    blogs = tools.paginator(request,queryset)

    category = tools.Topics().category
    subcategory = tools.Topics().subcatecory
    category2 = tools.Topics().category2

    output = dict(
        blog = blogs,
        topics_category = category,
    )

    return render(request,"blog/blogs.html",output)
