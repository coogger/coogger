from django.http import *
from django.shortcuts import render
from django.contrib import messages as ms
from cooggerapp.models import *
from django.db.models import Q
from cooggerapp.views import tools


def topic(request,topic):
    top = tools.Topics()
    category = top.category
    subcategory = top.subcatecory
    category2 = top.category2
    topi = category+subcategory+category2
    topics_list = [url for url,top in topi]
    if topic not in topics_list:
         ms.error(request,"Böyle bir konu bulunmamakta")
         return HttpResponseRedirect("/")
    queryset = False
    data1 = Blog.objects.filter(category = topic)
    data2 = Blog.objects.filter(subcategory = topic)
    data3 = Blog.objects.filter(category2 = topic)
    data = [data1,data2,data3]
    for dat in data:
        if dat.exists():
            queryset = dat
    if not queryset:
        ms.error(request,"Bu konu altında henuz bir şey paylaşılmamış")
        return HttpResponseRedirect("/")
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
    elastic_search = dict(
     title = topic+" | coogger",
     keywords = topic+"coogger "+topic,
     description = "coogger "+topic+" konulu içerikler"
    )
    output = dict(
        blog = blogs,
        topics_another = subcategory+category2,
        topics_category = top.category,
        elastic_search = elastic_search,
        general = True,
        paginator = paginator,
    )
    return render(request,"blog/blogs.html",output)
