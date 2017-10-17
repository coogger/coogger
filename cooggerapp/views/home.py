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
    blogs = tools.paginator(request,queryset,10)
    paginator = blogs
    pp = tools.get_pp(blogs)
    stars = []
    for i in blogs:
        try:
            stars.append(str(int(i.stars/i.hmstars)+1))
        except ZeroDivisionError:
            stars.append("0")
    ads = [ad for ad in range(1,21)]
    blogs = zip(blogs,pp,stars,ads)
    tools_topic = tools.Topics()
    category = tools_topic.category
    subcategory = {}
    for url,topic in category:
        sub_data = tools.take_subcategory(request,url,permission=True)
        if sub_data == None:
            continue
        for sub in sub_data:
            try:
                subcategory[topic].append(sub[0].lower())
            except KeyError:
                subcategory[topic] = []
                subcategory[topic].append(sub[0].lower())
    output = dict(
        blog = blogs,
        nav_category = category,
        nav_subcategory = subcategory,
        general = True,
        username = username,
        paginator = paginator,
    )
    return render(request,"blog/blogs.html",output)
