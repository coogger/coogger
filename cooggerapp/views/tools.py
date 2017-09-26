from cooggerapp.blog_topics import *
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render

class Topics():
    def __init__(self):
        self.category = Category().category
        self.subcatecory = Subcategory.all()
        self.category2 = Category2.all()

    def category(self):
        dict_topics = dict(
            url = [],
            topic = []
        )
        for top in self.category:
            dict_topics["url"].append(top[0])
            dict_topics["topic"].append(top[1])
        topics = zip(dict_topics["url"],dict_topics["topic"])
        return topics

    def subcatecory(self):
        dict_topics = dict(
            url = [],
            topic = []
        )
        for top in self.subcatecory:
            dict_topics["url"].append(top[0])
            dict_topics["topic"].append(top[1])
        topics = zip(dict_topics["url"],dict_topics["topic"])
        return topics

    def catecory2(self):
        dict_topics = dict(
            url = [],
            topic = []
        )
        for top in self.catecory2:
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