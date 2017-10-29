from django.http import *
from django.shortcuts import render
from django.contrib.auth import *
from django.contrib import messages
from django.db.models import F
from cooggerapp.models import Blog
from cooggerapp.views import tools

def home(request):
    return render(request,"blog/blogs.html",blog(request))

def blog(request):
    queryset = Blog.objects.all()
    blogs = tools.paginator(request,queryset,10)
    paginator = blogs
    pp = tools.get_pp(blogs)
    stars = []
    for i in blogs:
        try:
            stars.append(str(int(i.stars/i.hmstars)+1))
        except ZeroDivisionError:
            stars.append("0")
    blogs = zip(blogs,pp,stars)
    tools_topic = tools.Topics()
    category = tools_topic.category
    output = dict(
        blog = blogs,
        nav_category = category,
        general = True,
        ogurl = request.META["PATH_INFO"],
        paginator = paginator,
    )
    return output