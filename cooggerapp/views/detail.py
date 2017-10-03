from django.http import *
from django.shortcuts import render
from django.contrib.auth import *
from django.contrib import messages
from django.contrib.auth.models import User
from cooggerapp.models import *
from cooggerapp.views import tools

def main_detail(request,blog_path,utopic,path,):
    "blogların detail kısmı "
    queryset = Blog.objects.filter(url = blog_path)[0]
    username = queryset.username
    category = tools.Topics().category
    user = User.objects.filter(username = username)
    pp = Author.objects.filter(user = user)[0].pp
    elastic_search = dict(
        title = username+" | "+utopic+" | "+queryset.title+" | coogger",
        keywords = queryset.tag +","+str(username)+",coogger "+str(username)+","+username+utopic+",coogger"+username+utopic+",coogger "+queryset.category+", "+queryset.title+",coogger ",
        description = "coogger | "+str(username)+" | "+utopic+" "+queryset.category+" "+queryset.title
    )
    output = dict(
        detail = queryset,
        elastic_search = elastic_search,
        general = True,
        pp = pp,
        topics_category = category,
    )
    return render(request,"detail/main_detail.html",output)
