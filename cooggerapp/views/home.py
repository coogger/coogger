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
    username = request.user.username
    blogs = tools.paginator(request,queryset)
    paginator = blogs
    pp = tools.get_pp(blogs)
    blogs = zip(blogs,pp)
    category = tools.Topics().category
    subcategory = tools.Topics().subcatecory
    category2 = tools.Topics().category2
    output = dict(
        blog = blogs,
        topics_category = category,
        topics_another = subcategory+category2,
        general = True,
        username = username,
        paginator = paginator,
    )
    return render(request,"blog/blogs.html",output)
