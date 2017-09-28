# content control 
from django.http import *
from django.shortcuts import render
from django.contrib.auth import *
from django.contrib import messages as ms
from cooggerapp.models import *
from django.contrib.auth.models import User
from cooggerapp.forms import *

def panel(request):
    "control panel for users"
    username = request.user.username 
    if not User.objects.filter(username=username).exists():
        ms.error(request,"Kontrol paneline erişmek için giriş yapın veya üye olun !")
        return HttpResponseRedirect("/")
    queryset = Blog.objects.filter(username = username)
    output = dict(
        username = username,
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
        tr = "şöüğıç"
        en = "sougic"
        title = request.POST.get("title")
        title = str(title).lower().replace(" ","-")
        for t,e in zip(tr,en):
            title = title.replace(t,e)
        url = title
        content.url = url
        content.save()
        return HttpResponseRedirect("/blogs/"+url)
    # get method
    output = dict(
        username = username,
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
        content.save()
        return HttpResponseRedirect("/blogs/"+queryset.url)
    # get method
    output = dict(
        username = username,
        controls = True,
        change = queryset,
        content_id = content_id,
        change_form = change_form,
    )
    return render(request,"controls/change.html",output)
            
def delete(request,content_id):
    "to delete the content"
    if not request.is_ajax():
        ms.error(request,"Girmek istediğiniz sayfa bulunamadı !")
        return HttpResponseRedirect("/")
    username = request.user.username 
    if not User.objects.filter(username=username).exists():
        ms.error(request,"İçerik silmek için giriş yapın veya üye olun !")
        return HttpResponseRedirect("/")
    try:
         queryset = Blog.objects.filter(username = username,id = content_id)
    except:
        ms.error(request,"Silmek istediğiniz nesne bulunamadı !")
        return HttpResponseRedirect("/control")
    if not queryset.exists():
        ms.error(request,"Girmek istediğiniz sayfada yönetim iznine sahip değilsiniz !")
        return HttpResponseRedirect("/")
    try:
        queryset = queryset.delete()
    except:
        return HttpResponse("Silme işlemi sırasında beklenmedik hata !")
    return HttpResponse("Silme işlemi başarılı ")

    
