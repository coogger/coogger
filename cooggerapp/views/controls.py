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
from cooggerapp.views import tools

def panel(request):
    "control panel for users"
    request_username = request.user.username 
    user_objects = User.objects.filter(username=request_username)
    if not user_objects.exists():
        ms.error(request,"Kontrol paneline erişmek için giriş yapın veya üye olun !")
        return HttpResponseRedirect("/")
    elif user_objects[0].is_superuser:
        queryset = Blog.objects.all()
    else:
        queryset = Blog.objects.filter(username = request_username)
    queryset = tools.paginator(request,queryset)
    output = dict(
        controls = True,
        paginator = queryset,
        contents = queryset,
        blog = queryset, # sayfalama yapabilmek için blog adında tekrar gönderdik veriyi 
    ) 
    return render(request,"controls/control.html",output)

def create(request): 
    "to create new content"
    request_username = request.user.username 
    if not User.objects.filter(username=request_username).exists():
        ms.error(request,"İçerik oluşturmak için giriş yapın veya üye olun !")
        return HttpResponseRedirect("/")
    create_form = ContentForm(request.POST or None)
    # post method
    if create_form.is_valid():
        content = create_form.save(commit=False)
        content.username = request_username
        content_list = slugify(request.POST["content_list"])
        content.content_list = content_list
        title = content.title
        url = slugify(title)
        content.url = "@"+request_username+"/"+content_list+"/blog/"+url
        content.dor = tools.durationofread(content.content+title)
        try:
            content_list_save = ContentList.objects.filter(username = request_username,content_list = content_list)[0]
            content_list_save.content_count = F("content_count")+1
            content_list_save.save()
            # kullanıcının açmış oldugu listeleri kayıt ediyoruz
        except: # önceden oluşmuş ise hata verir ve biz 1 olarak kayıt ederiz
            ContentList(username = request_username,content_list = content_list,content_count = 1).save()
        content.save()
        return HttpResponseRedirect("/@"+request_username+"/"+content_list+"/blog/"+url)
    # get method
    output = dict(
        controls = True,
        create_form = create_form,
    )
    return render(request,"controls/create.html",output)

def change(request,content_id):
    "to change the content"
    request_username = request.user.username 
    if not request_username:
        ms.error(request,"Düzenleme yapmak için giriş yapın veya üye olun !")
        return HttpResponseRedirect("/")
    elif User.objects.filter(username=request_username)[0].is_superuser:
        queryset = Blog.objects.filter(id = content_id)
    else:
        queryset = Blog.objects.filter(username = request_username,id = content_id)
    real_username = queryset[0].username # içeriği yazan kişinin kullanıcı ismi
    if not queryset.exists():
        ms.error(request,"Girmek istediğiniz sayfada yönetim iznine sahip değilsiniz !")
        return HttpResponseRedirect("/")
    queryset = queryset[0]
    old_content_list = str(queryset.content_list)
    change_form = ContentForm(request.POST or None,instance=queryset)
    # post method
    if change_form.is_valid():
        content = change_form.save(commit=False)
        content.username = real_username
        content_list = str(slugify(request.POST["content_list"]))
        content.content_list = content_list
        content.time = queryset.time
        title = content.title
        url = slugify(title)
        content.url = "@"+real_username+"/"+content_list+"/blog/"+url 
        content.dor = tools.durationofread(content.content+title) 
        content.save()
        if content_list != old_content_list: # content_list değişmiş ise
            try:
                content_list_save = ContentList.objects.filter(username = real_username,content_list = old_content_list)[0]
                content_list_save.content_count = F("content_count")-1 # eskisini bir azaltıyor
                content_list_save.save()
                try:
                    ContentList.objects.filter(content_count = 0)[0].delete() # sıfır olanı siliyor
                except IndexError:
                    pass
            except IndexError:
                pass
        try:
            content_list_save = ContentList.objects.filter(username = real_username,content_list = content_list)[0]
            content_list_save.content_count = F("content_count")+1 # zaten bu isim varsa bir artırıyor
            content_list_save.save()
        except IndexError:
            ContentList(username = real_username,content_list = content_list,content_count = 1).save() # yoksa yeni bir tane acıyor
        return HttpResponseRedirect("/@"+real_username+"/"+content_list+"/blog/"+url)
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
    elif User.objects.filter(username=request_username)[0].is_superuser: # admin
        queryset = Blog.objects.filter(id = content_id) 
    else:
        queryset = Blog.objects.filter(username = request_username,id = content_id)
    real_username = queryset[0].username # içeriği yazan kişinin kullanıcı ismi
    if not queryset.exists():
        ms.error(request,"Girmek istediğiniz sayfada yönetim iznine sahip değilsiniz !")
        return HttpResponseRedirect("/")
    content_list = queryset[0].content_list
    try:
        queryset.delete()
        try:
            content_list_save = ContentList.objects.filter(username = real_username,content_list = content_list)[0]
            content_list_save.content_count = F("content_count")-1
            content_list_save.save()
            try:
                ContentList.objects.filter(content_count = 0)[0].delete()
            except:
                pass
        except:
            return HttpResponse("Nesne silindi fakat content list hatası meydana geldi !")
    except:
        return HttpResponse("Silme işlemi sırasında beklenmedik hata !")
    return HttpResponse("Silme işlemi başarılı ")