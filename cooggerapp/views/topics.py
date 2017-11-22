from django.http import *
from django.shortcuts import render
from django.contrib import messages as ms
from cooggerapp.models import Blog
from django.db.models import Q
from cooggerapp.views.tools import Topics,get_head_img_pp
from cooggerapp.views.home import content_cards


def topic(request,topic):
    queryset = look_at_topics(request,topic)
    if queryset == None:
        ms.error(request,"{} isimde bir konu coogger.com'da mevcut değil.".format(topic))
        return HttpResponseRedirect("/")
    else:
        if not queryset.exists():
            ms.error(request,"{} isimli konu altında henuz bir şey paylaşılmamış".format(topic))
            return HttpResponseRedirect("/")
    info_of_cards = content_cards(request,queryset)
    nameofexplain = queryset[0].category
    try:
        img_pp = get_head_img_pp(request.user)
    except:
        img_pp = ["/static/media/profil.png",None]
    elastic_search = dict(
     title = topic+" | coogger",
     keywords = topic+"coogger "+topic,
     description = "coogger "+topic+" konulu içerikler",
     img="/static/media/topics/"+nameofexplain+".svg",
    )
    output = dict(
        blog = info_of_cards[0],
        elastic_search = elastic_search,
        general = True,
        img = img_pp[0],
        nameoftopic = topic,
        nameofexplain = nameofexplain,
        ogurl = request.META["PATH_INFO"],
        nav_category = Topics().category_slug ,
        paginator = info_of_cards[1],
    )
    return render(request,"blog/blogs.html",output)

def look_at_topics(request,topic):
    "gelen topic (konu) bilgisine göre konu varmı yokmu bakar hangi bölümde oldugunu bulur ilgili querysetı cıktı olarak verir"
    top = Topics()
    category_url = [url for url,title in top.category]
    subcategory_url = [url for url,title in top.subcatecory]
    loop_number = 0
    queryset = None
    for all_topic_url in [category_url,subcategory_url]:
        loop_number += 1
        for topic_url in all_topic_url:
            if topic_url == topic:
                if loop_number == 1:
                    queryset = Blog.objects.filter(category = topic)
                elif loop_number == 2:
                    queryset = Blog.objects.filter(subcategory = topic)
    return queryset
