from django.http import *
from django.shortcuts import render
from django.contrib import messages as ms
from cooggerapp.models import *
from django.db.models import Q
from cooggerapp.views import tools


def topic(request,topic):
    model = Blog 
    topics_list = [url for url,top in tools.topics()]
    if topic.replace(" ","_") not in topics_list:
         ms.error(request,"Böyle bir konu bulunmamakta")
         return HttpResponseRedirect("/")
    try:
        queryset = model.objects.filter(category = topic)
    except:
         try:
             queryset = model.objects.filter(category = topic)
         except:
             try:
                 queryset = model.objects.filter(category = topic)
             except:
                 return HttpResponseRedirect("/")
    if not queryset.exists():
        ms.error(request,"Bu konu altında henuz bir şey paylaşılmamış")
        return HttpResponseRedirect("/")
    blogs = tools.paginator(request,queryset)
    elastic_search = dict(
     title = "coogger | "+topic,
     keywords = "coogger,konu,"+topic+",topic,"+"coogger "+topic,
     description = "coogger a hoşgeldiniz ,"+topic+" konulu içerikler burada bulunur"
    )
    output = dict(
        blog = blogs,
        topics = tools.topics(),
        elastic_search = elastic_search,
    )
    return render(request,"blog/blogs.html",output)