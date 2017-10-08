from django.http import *
from django.shortcuts import render
from django.contrib.auth import *
from django.contrib import messages
from django.db.models import F
from cooggerapp.models import *
from cooggerapp.forms import *
from cooggerapp.views import tools

def home(request):
    queryset = Blog.objects.all()
    username = request.user.username
    blogs = tools.paginator(request,queryset)
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
    subcategory = tools_topic.subcatecory
    category2 = tools_topic.category2
    output = dict(
        blog = blogs,
        topics_category = category,
        topics_another = subcategory+category2,
        general = True,
        username = username,
        paginator = paginator,
    )
    return render(request,"blog/blogs.html",output)
