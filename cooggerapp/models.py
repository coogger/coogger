from django.db import models
from django.utils import timezone
from ckeditor.fields import RichTextField 
from cooggerapp.blog_topics import *
from django.contrib.auth.models import User
from cooggerapp.views import tools

class Blog(models.Model): # blog için yazdığım yazıların tüm bilgisi  
    username = models.CharField(max_length=37)
    content_list = models.CharField(max_length=30,verbose_name ="İçeriğinizin liste ismini yazın")
    category = models.CharField(choices = Category().category ,max_length=30,verbose_name ="Kategori") 
    subcategory = models.CharField(blank=True, null=True,choices = Subcategory.all() ,max_length=50,verbose_name ="Alt kategori") # konu belirleme yanı bu yazı yazılımlamı ilgili elektriklemi , bu sayede ilgili yere gidebilecek
    category2 = models.CharField(blank=True, null=True,choices = Category2.all() ,max_length=80,verbose_name = "İkinci alt kategori")
    title = models.CharField(max_length=100,verbose_name = "Başlık yazın") # başlık bilgisi ama sadece admin de içiriğin ne oldugunu anlamak için yaptım
    url = models.SlugField(unique = True ,max_length=100,verbose_name = "Web adresi, başlık ile aynı olmasına özen gösterin ") # blogun url adresi 
    content = RichTextField(verbose_name = "içeriğinizi oluşturun")  # yazılan yazılar burda 
    tag = models.CharField(max_length=100,verbose_name = "İçeriğiniz ili ilgili anahtar kelimeleri virgul kullanarak yazın") # taglar konuyu ilgilendiren içeriği anlatan kısa isimler google aramalarında çıkması için
    time = models.DateTimeField(default = timezone.now,verbose_name="tarih") # tarih bilgisi 
    class Meta:
        verbose_name = "content"
        ordering = ['-time']

class ContentList(models.Model): # kullanıcıların sahip oldukları listeler
    username = models.CharField(max_length=37)
    content_list = models.SlugField(max_length=30,verbose_name ="İçerik listeniz")
    content_count = models.IntegerField(verbose_name = "liste içindeki nesne sayısı")

class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    iban = models.CharField(max_length=24)

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
