from cooggerapp.blog_topics import *
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render

def topics():
    dict_topics = dict(
        url = [],
        topic = []
    )
    topics = Category().category + Subcategory.all() + Category2.all()
    for top in topics:
        dict_topics["url"].append(top[0])
        dict_topics["topic"].append(top[1])
    topics = zip(dict_topics["url"],dict_topics["topic"])
    return topics

def paginator(request,queryset,hmany=20): 
    paginator = Paginator(queryset, hmany) 
    page = request.GET.get('page')
    try:
        contacts = paginator.page(page)
    except PageNotAnInteger:
        contacts = paginator.page(1)
    except EmptyPage:
        contacts = paginator.page(paginator.num_pages)
    return contacts

def seo(request): 
    "arama motoru optimizasyonu için robot.txt ve site haritası"
    file = request.get_full_path()
    return render(request,"seo/"+file,{})