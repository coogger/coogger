from django.http import *
from django.shortcuts import render
from django.contrib.auth import *
from django.contrib import messages
from django.db.models import F
from cooggerapp.models import *
from cooggerapp.forms import *
from cooggerapp.blog_topics import *

def home(request):
    queryset = Blog.objects.all()
    topics = Category().category + Subcategory.all() + Category2.all()
    dict_topics = dict(
        url = [],
        topic = []
    )
    for top in topics:
        dict_topics["url"].append(top[0])
        dict_topics["topic"].append(top[1])
    topics = zip(dict_topics["url"],dict_topics["topic"])
    output = dict(
        blog = queryset,
        topics = topics,
    )
    return render(request,"blog/blogs.html",output)
