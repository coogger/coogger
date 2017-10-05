from django.http import *
from django.shortcuts import render
from django.contrib.auth import *
from django.contrib import messages
from django.contrib.auth.models import User
from cooggerapp.models import *
from cooggerapp.views import tools
from django.db.models import F
from django.contrib.auth.models import User

def main_detail(request,blog_path,utopic,path,):
    "blogların detail kısmı "
    queryset = Blog.objects.filter(url = blog_path)[0]
    username = queryset.username
    category = tools.Topics().category
    subcategory = tools.Topics().subcatecory
    category2 = tools.Topics().category2
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
        topics_another = subcategory+category2,
        pp = pp,
        stars = str(int(queryset.stars)),
        topics_category = category,
    )
    return render(request,"detail/main_detail.html",output)

def stars(request,post_id,stars_id):
    request_username = request.user.username 
    if not User.objects.filter(username=request_username).exists():
        return HttpResponse("Giriş yapın veya üye olun")
    queryset = Blog.objects.filter(id = post_id)[0]
    queryset.stars = F("stars")+stars_id
    queryset.save()
    stars = queryset.stars + stars_id
    first_li = """<li class="d-starts-li" data-starts-id="{{i}}" data-post-id="""+ post_id+ """>
            <img class="d-starts-a" src="/static/media/icons/star.svg">
            </li>"""
    second_li="""<li class="d-starts-li" data-starts-id="{{i}}" data-post-id="""+ post_id+ """>
                <img class="d-starts-a" src="/static/media/icons/star({{i}}).svg">
            </li>"""
    output = ""
    for i in "0123456789":
        if i <= str(stars_id):
            output += first_li.replace("{{i}}",i)
        if i > str(stars_id):
            output += second_li.replace("{{i}}",i)
    return HttpResponse(output)

