# content control 
from django.http import *
from django.shortcuts import render
from django.contrib.auth import *
from django.contrib import messages as ms
from cooggerapp.models import *
from django.contrib.auth.models import User
from cooggerapp.forms import *
from django.db.models import F
from django.utils.text import slugify

def panel(request):
    "control panel for users"
    username = request.user.username 
    if not User.objects.filter(username=username).exists():
        ms.error(request,"Kontrol paneline erişmek için giriş yapın veya üye olun !")
        return HttpResponseRedirect("/")
    queryset = Blog.objects.filter(username = username)
    output = dict(
        controls = True,
        contents = queryset,
    )
    return render(request,"controls/control.html",output)

def create(request): 
    "to create new content"
    username = request.user.username 
    if not User.objects.filter(username=username).exists():
        ms.error(request,"İçerik oluşturmak için giriş yapın veya üye olun !")
        return HttpResponseRedirect("/")
    create_form = ContentForm(request.POST or None)
    # post method
    if create_form.is_valid():
        content = create_form.save(commit=False)
        content.username = username
        content_list = request.POST["content_list"]
        content.content_list = slugify(content_list)
        url = slugify(username+"-"+content_list+"-"+content.title)
        content.url = url
        try:
            content_list_save = ContentList.objects.filter(username = username,content_list = content_list)[0]
            content_list_save.content_count = F("content_count")+1
            content_list_save.save()
            # kullanıcının açmış oldugu listeleri kayıt ediyoruz
        except: # önceden oluşmuş ise hata verir ve biz 1 olarak kayıt ederiz
            ContentList(username = username,content_list = content_list,content_count = 1).save()
        content.save()
        return HttpResponseRedirect("/blogs/"+url)
    # get method
    output = dict(
        controls = True,
        create_form = create_form,
    )
    return render(request,"controls/create.html",output)

def change(request,content_id):
    "to change the content"
    username = request.user.username 
    if not User.objects.filter(username=username).exists():
        ms.error(request,"Düzenleme yapmak için giriş yapın veya üye olun !")
        return HttpResponseRedirect("/")
    try:
         queryset = Blog.objects.filter(username = username,id = content_id)
    except:
        ms.error(request,"Silmek istediğiniz nesne bulunamadı !")
        return HttpResponseRedirect("/control")
    if not queryset.exists():
        ms.error(request,"Girmek istediğiniz sayfada yönetim iznine sahip değilsiniz !")
        return HttpResponseRedirect("/")
    queryset = queryset[0]
    change_form = ContentForm(request.POST or None,instance=queryset)
    # post method
    if change_form.is_valid():
        content = change_form.save(commit=False)
        content.username = username
        content.time = queryset.time
        content.url = queryset.url
        content_list = request.POST["content_list"]
        content.content_list = slugify(content_list)
        try:
            content_list_save = ContentList.objects.filter(username = username,content_list = content_list)[0]
        except:
            ContentList(username = username,content_list = content_list,content_count = 1).save()
        content.save()
        return HttpResponseRedirect("/blogs/"+queryset.url)
    # get method
    output = dict(
        controls = True,
        change = queryset,
        content_id = content_id,
        change_form = change_form,
    )
    return render(request,"controls/change.html",output)
            
def delete(request,content_id):
    "to delete the content"
    request_username = request.user.username
    if not request.is_ajax():
        ms.error(request,"ops !")
        return HttpResponseRedirect("/")
    elif not request_username:
        ms.error(request,"Silme işleminden önce giriş yapmalısınız !")
        return HttpResponseRedirect("/")
    queryset = Blog.objects.filter(username = request_username,id = content_id)
    if not queryset.exists():
        ms.error(request,"Girmek istediğiniz sayfada yönetim iznine sahip değilsiniz !")
        return HttpResponseRedirect("/")
    try:
        content_list = queryset[0].content_list
        queryset.delete()
        content_list_save = ContentList.objects.filter(username = request_username,content_list = content_list)[0]
        content_list_save.content_count = F("content_count")-1
        content_list_save.save()
        ContentList.objects.filter(content_count = 0)[0].delete()
    except:
        return HttpResponse("Silme işlemi sırasında beklenmedik hata !")
    return HttpResponse("Silme işlemi başarılı ")
