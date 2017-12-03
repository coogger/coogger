from ckeditor.fields import RichTextField
from cooggerapp.choices import *
from cooggerapp.views.tools import Topics,make_choices
from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


class Blog(models.Model): # blog için yazdığım yazıların tüm bilgisi
    tools_topic = Topics()
    choices_category = tools_topic.category
    choices_subcategory = tools_topic.subcatecory
    username = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    content_list = models.CharField(blank=True, null=True,max_length=30,verbose_name ="Liste ismi")
    category = models.CharField(choices = choices_category ,max_length=30,verbose_name ="Fakülteler")
    subcategory = models.CharField(blank=True, null=True,choices=choices_subcategory,max_length=50,verbose_name ="Bölümler") # konu belirleme yanı bu yazı yazılımlamı ilgili elektriklemi , bu sayede ilgili yere gidebilecek
    title = models.CharField(max_length=100,verbose_name = "Başlık yazın") # başlık bilgisi ama sadece admin de içiriğin ne oldugunu anlamak için yaptım
    url = models.SlugField(unique = True ,max_length=100,verbose_name = "web adresi") # blogun url adresi
    content = RichTextField(verbose_name = "İçeriğinizi yazın")  # yazılan yazılar burda
    show = models.CharField(max_length=400,verbose_name = "Anasayfa'da görünecek içerik notu ekleyin")
    tag = models.CharField(max_length=200,verbose_name = "Virgül kullanarak anahtar kelimeleri yazın") # taglar konuyu ilgilendiren içeriği anlatan kısa isimler google aramalarında çıkması için
    time = models.DateTimeField(default = timezone.now,verbose_name="tarih") # tarih bilgisi
    dor = models.TextField(default = 0, verbose_name = "duration of read")
    stars = models.IntegerField(default = 0, verbose_name = "Yıldız")
    hmstars = models.IntegerField(default = 0,verbose_name = "kaç kişi oy kullandı")
    views = models.IntegerField(default = 0,verbose_name = "görüntülenme sayısı") # görütülenme sayısını kayıt eder
    hmanycomment=models.IntegerField(default = 0,verbose_name = "yorum sayısı")
    class Meta:
        verbose_name = "content"
        ordering = ['-time']

class Blogviews(models.Model): # görüntülenme ip ve blog_id bilgisini kayıt eder
    content = models.ForeignKey("Blog", on_delete=models.CASCADE)
    ip = models.CharField(max_length=200)

class Voters(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    blog = models.ForeignKey("Blog",verbose_name = "hangi blog")
    star = models.IntegerField(default = 0, verbose_name = "Yıldız")


class ContentList(models.Model): # kullanıcıların sahip oldukları listeler
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    content_list = models.SlugField(max_length=30,verbose_name ="İçerik listeniz")
    content_count = models.IntegerField(verbose_name = "liste içindeki nesne sayısı")

class Author(models.Model): # yazarlık bilgileri
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    choices_sex = (
        ("male","erkek"),
        ("female","kadın"),
    )
    choices_country = make_choices(country())

    old = [i for i in range(1905,2017)]
    choices_old = make_choices(old)
    choices_university = make_choices(university())
    choices_jop = make_choices(jop())
    sex = models.CharField(choices = choices_sex,max_length=6,verbose_name="cinsiyet")
    county = models.CharField(choices = choices_country,max_length=50,verbose_name="memleket")
    old = models.CharField(choices = choices_old,verbose_name="doğum tarihin",max_length=4)
    university = models.CharField(null=True,choices = choices_university,verbose_name="üniversite",max_length=100)
    jop = models.CharField(null=True,choices = choices_jop,verbose_name="meslek",max_length=30) # boş olamaz uni yazmamış ise öğrenci olarak seçer
    phone = models.IntegerField(blank=True, null=True,unique = True,verbose_name = "telefon numarası")

class OtherInformationOfUsers(models.Model): # kullanıcıların diğer bilgileri
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    pp = models.BooleanField(verbose_name = "profil resmi yüklemiş mi ?") # profil resmi yüklemişmi
    is_author = models.BooleanField(verbose_name = "yazar olarak kabul et") # onaylanıp onaylanmadıgı
    author = models.BooleanField(verbose_name = "yazarlık başvurusu yaptımı") # yazar başvurusu yaptımı ?

class UserFollow(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    choices = models.CharField(max_length=15, choices = make_choices(follow()),verbose_name="Web sitesi")
    adress = models.CharField(max_length=150,verbose_name = "Adresi yazın")

class Comment(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE,verbose_name="yorum yapan kişi")
    content = models.ForeignKey("Blog", on_delete=models.CASCADE,verbose_name="hangi içeriğe yorum yapmış")
    date = models.DateTimeField(default = timezone.now,verbose_name="tarih")
    comment = models.CharField(max_length=310,verbose_name="Soru sor veya teşekkür et, yorum yap")

class Notification(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE,verbose_name="bildirimin gittiği kişi")
    even = models.IntegerField(verbose_name="bildirime sebeb olan olay numarası")
    content = models.CharField(max_length=310,verbose_name="bildirim mesajı")
    show = models.BooleanField(default=False,verbose_name="gördü/görmedi")
    address = models.SlugField(verbose_name="bildirimin gerçekleştiği adres")
    time = models.DateTimeField(default = timezone.now,verbose_name="tarih")

class SearchedWords(models.Model):
    word = models.CharField(unique=True,max_length=310,verbose_name="aranan kelime")
    hmany = models.IntegerField(default = 1,verbose_name="kaç defa arandı")
