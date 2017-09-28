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
    user_id = User.objects.filter(username =username)[0].id
    queryset = Blog.objects.filter(username = user_id)
    output = dict(
        username = username,
        controls = True,
        contents = queryset,
    )
    return render(request,"controls/control.html",output)

def create(request): 
    "to create new content"
    try:
        username = request.user.username 
        user_id = User.objects.filter(username = username)[0].id 
    except:
        ms.error(request,"İçerik oluşturmak için giriş yapın veya üye olun !")
        return HttpResponseRedirect("/")
    create_form = ContentForm(request.POST or None)
    # post method
    if create_form.is_valid():
        content = create_form.save(commit=False)
        content.username = username
        tr = ["ş","ö","ü","ğ","ı","ç"]
        en = ["s","o","u","g","i","c"]
        url = request.GET.get("title").lower().replace(" ","-")
        for t,e in zip(tr,en):
            url = url.replace(tr,en)
        content.url = url
        content.save()
        return HttpResponseRedirect("/blogs/"+queryset.url)
    # get method
    output = dict(
        username = username,
        controls = True,
        create_form = create_form,
    )
    return render(request,"controls/create.html",output)

def change(request,content_id):
    "to change the content"
    try:
        username = request.user.username 
        user_id = User.objects.filter(username = username)[0].id 
    except:
        ms.error(request,"Düzenleme yapmak istediğiniz içerik size ait ise önce giriş yapmalısınız !")
        return HttpResponseRedirect("/")
    if not Blog.objects.filter(username = user_id,id = content_id).exists():
        ms.error(request,"Girmek istediğiniz sayfada yönetim iznine sahip değilsiniz !")
        return HttpResponseRedirect("/")
    queryset = Blog.objects.filter(id = content_id)[0]
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
    try:
        username = request.user.username 
        user_id = User.objects.filter(username = username)[0].id 
    except:
        ms.error(request,"Düzenleme yapmak istediğiniz içerik size ait ise önce giriş yapmalısınız !")
        return HttpResponseRedirect("/")
    if not Blog.objects.filter(username = user_id,id = content_id).exists():
        ms.error(request,"Girmek istediğiniz sayfada yönetim iznine sahip değilsiniz !")
        return HttpResponseRedirect("/")
    try:
        queryset = Blog.objects.filter(id = content_id).delete()
    except:
        ms.error(request,"Silme sırasında beklenmedik bir sorun oluştu")
        return HttpResponseRedirect("/control/")
    ms.error(request,"İçerik silme başarılı")
    return HttpResponseRedirect("/control/")


    
