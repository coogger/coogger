from django.http import *
from django.shortcuts import render
from django.contrib.auth import *
from django.contrib import messages
from django.contrib.auth.models import User
from cooggerapp.models import Blog,Views,OtherInformationOfUsers
from cooggerapp.views import tools
from django.db.models import F
from django.contrib.auth.models import User
from bs4 import BeautifulSoup

def main_detail(request,blog_path,utopic,path,):
    "blogların detail kısmı "
    queryset = Blog.objects.filter(url = blog_path)[0]
    username = queryset.username
    ip = request.META['REMOTE_ADDR'] 
    model_views = Views.objects.filter(blog_id = queryset.id,ip = ip)
    if not model_views.exists():
        Views(blog_id = queryset.id ,ip = ip).save()
        queryset.views = F("views") + 1
        queryset.save()  
        queryset = Blog.objects.filter(url = blog_path)[0]      
    category = tools.Topics().category
    user = User.objects.filter(username = username)
    pp = OtherInformationOfUsers.objects.filter(user = user)[0].pp
    try:
        stars = str(int(queryset.stars/queryset.hmstars))
    except ZeroDivisionError:
        stars = ""
    description = BeautifulSoup(queryset.show, 'html.parser').get_text()
    another_content = Blog.objects.filter(username = username,content_list = utopic)
    nav_category = []
    for content in another_content:
        nav_category.append((content.url,content.title))
    elastic_search = dict(
        title = queryset.title+" | coogger",
        keywords = queryset.tag +","+username+" "+utopic+", "+utopic+",coogger "+queryset.category+", "+queryset.title,
        description = description,
    )
    output = dict(
        detail = queryset,
        elastic_search = elastic_search,
        general = True,
        pp = pp,
        stars = stars,
        nameoftopic = queryset.title,
        nav_category = nav_category,
        nameoflist = utopic,
    )
    return render(request,"detail/main_detail.html",output)

def stars(request,post_id,stars_id):
    if not request.is_ajax():
        return None
    request_username = request.user.username 
    user = User.objects.filter(username=request_username)
    blog = Blog.objects.filter(id = post_id)[0]
    if not user.exists():
        return HttpResponse("Oy vermek için giriş yapmalı veya üye olmalısınız")
    try:
        vot = Voters.objects.filter(username_id = user[0].id,blog_id = blog.id) # daha önceden verdiği oy varsa alıyoruz
        old = vot[0].star
        vot.update(star = stars_id)
        blog.stars = F("stars")-old+stars_id
        blog.save()
    except IndexError: # ilk kez oylama yapıyor
        Voters(username_id = user[0].id,blog_id = blog.id,star = stars_id).save()
        blog.hmstars = F("hmstars")+1
        blog.stars = F("stars")+stars_id
        blog.save()         
    first_li = """<li class="d-starts-li" data-starts-id="{{i}}" data-post-id="""+ post_id+ """>
            <img class="d-starts-a" src="/static/media/icons/star.svg">
            </li>"""
    second_li="""<li class="d-starts-li" data-starts-id="{{i}}" data-post-id="""+ post_id+ """>
                <img class="d-starts-a" src="/static/media/icons/star({{i}}).svg">
            </li>"""
    output = ""
    blog = Blog.objects.filter(id = post_id)[0]
    stars = blog.stars
    hmstars = blog.hmstars
    rate = stars/hmstars
    for i in range(0,10):
        if i <= int(rate):
            output += first_li.replace("{{i}}",str(i))
        if i > int(rate):
            output += second_li.replace("{{i}}",str(i))
        if i == 9:
            output +="<li> : "+str(hmstars)+"</li>"
    return HttpResponse(output)

