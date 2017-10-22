from django.db import models
from django.utils import timezone
from ckeditor.fields import RichTextField 
from cooggerapp.choices import *
from django.contrib.auth.models import User
from cooggerapp.views.tools import Topics,make_choices
from cooggerapp.choices import *

class Blog(models.Model): # blog için yazdığım yazıların tüm bilgisi  
    tools_topic = Topics()
    choices_category = tools_topic.category
    choices_subcategory = tools_topic.subcatecory
    choices_category2 = tools_topic.category2
    username = models.CharField(max_length=37)
    content_list = models.CharField(max_length=30,verbose_name ="Liste ismi")
    category = models.CharField(choices = choices_category ,max_length=30,verbose_name ="Kategori") 
    subcategory = models.CharField(blank=True, null=True,choices=choices_subcategory,max_length=50,verbose_name ="Alt kategori") # konu belirleme yanı bu yazı yazılımlamı ilgili elektriklemi , bu sayede ilgili yere gidebilecek
    category2 = models.CharField(blank=True, null=True,choices=choices_category2,max_length=80,verbose_name = "İkinci alt kategori")
    title = models.CharField(max_length=100,verbose_name = "Başlık yazın") # başlık bilgisi ama sadece admin de içiriğin ne oldugunu anlamak için yaptım
    url = models.SlugField(unique = True ,max_length=100,verbose_name = "web adresi") # blogun url adresi 
    content = RichTextField(verbose_name = "İçeriğinizi yazın")  # yazılan yazılar burda 
    show = models.CharField(max_length=400,verbose_name = "Anasayfa'da görünecek içerik notu ekleyin")
    tag = models.CharField(max_length=200,verbose_name = "Virgül kullanarak ahtar kelimeleri yazın") # taglar konuyu ilgilendiren içeriği anlatan kısa isimler google aramalarında çıkması için
    time = models.DateTimeField(default = timezone.now,verbose_name="tarih") # tarih bilgisi 
    dor = models.TextField() # duration of read içerik okuma süresi
    stars = models.IntegerField(default = 0, verbose_name = "Yıldız")
    hmstars = models.IntegerField(default = 0,verbose_name = "kaç kişi oy kullandı")
    views = models.IntegerField(default = 0,verbose_name = "görüntülenme sayısı") # görütülenme sayısını kayıt eder
    class Meta:
        verbose_name = "content"
        ordering = ['-time']

class Views(models.Model): # görüntülenme ip ve blog_id bilgisini kayıt eder
    blog_id = models.IntegerField()
    ip = models.CharField(max_length=200)

class Voters(models.Model):
    username_id = models.IntegerField()
    blog_id = models.IntegerField(verbose_name = "hangi blog")
    star = models.IntegerField(default = 0, verbose_name = "Yıldız")


class ContentList(models.Model): # kullanıcıların sahip oldukları listeler
    username = models.CharField(max_length=37)
    content_list = models.SlugField(max_length=30,verbose_name ="İçerik listeniz")
    content_count = models.IntegerField(verbose_name = "liste içindeki nesne sayısı")

class Author(models.Model): # yazarlık bilgileri
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    choices_sex = (
        ("male","erkek"),
        ("female","kadın"),
    )
    choices_country = make_choices(Subcategory.seyahat())
    old = [i for i in range(1905,2017)]
    choices_old = make_choices(old)
    choices_university = make_choices(university())
    choices_jop = make_choices(jop())
    sex = models.CharField(choices = choices_sex,max_length=6,verbose_name="cinsiyet")
    county = models.CharField(choices = choices_country,max_length=50,verbose_name="memleket")
    old = models.CharField(choices = choices_old,verbose_name="doğum tarihin",max_length=4)
    university = models.CharField(null=True,choices = choices_university,verbose_name="üniversite",max_length=100)
    jop = models.CharField(null=True,choices = choices_jop,verbose_name="meslek",max_length=30) # boş olamaz uni yazmamış ise öğrenci olarak seçer 
    #iban = models.CharField(unique = True,max_length=24,null=True,verbose_name = "kart iban numarası")
    phone = models.IntegerField(unique = True,verbose_name = "telefon numarası")

class OtherInformationOfUsers(models.Model): # kullanıcıların diğer bilgileri
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    pp = models.BooleanField(verbose_name = "profil resmi yüklemiş mi ?") # profil resmi yüklemişmi
    is_author = models.BooleanField(verbose_name = "yazar olarak kabul et") # onaylanıp onaylanmadıgı
    author = models.BooleanField(verbose_name = "yazarlık başvurusu yaptımı") # yazar başvurusu yaptımı ?

class UserFollow(models.Model):
    choices_user = make_choices(users())
    user = models.CharField(choices = choices_user,max_length=37)
    choices = models.CharField(max_length=15, choices = make_choices(follow()))
    adress = models.CharField(max_length=150,verbose_name = "Adresi yazın")




"""# ------------------------------------
class Comment(models.Model): # yapılan yorumlar
    username = models.CharField(max_length=100)
    url = models.SlugField(unique = True ,max_length=100)
    comment = models.CharField(max_length=210)
    hmcomment = models.IntegerField() # yapılan yorum sayısı 
    time = models.DateTimeField(default=timezone.now) # tarih bilgisi 


class Like(models.Model): # beğenme beğenmeme olayları
    username = models.CharField(max_length=100)
    url = models.SlugField(unique = True ,max_length=100)
    hmlike = models.IntegerField() # beğenilme sayısı 
    hmdislike = models.IntegerField() # beğenilmeme sayısı
    time = models.DateTimeField(default=timezone.now) # tarih bilgisi 


class Bookmark(models.Model): # beğendiği yazıları daha sonra okuması için kayıt etme özelliği
    username = models.CharField(max_length=100)
    url = models.SlugField(unique = True ,max_length=100)
    time = models.DateTimeField(default=timezone.now) # tarih bilgisi 
"""
