from django.db import models
from django.utils import timezone
from ckeditor.fields import RichTextField 
from blogapp.content_topics import *

class Content(models.Model): # blog için yazdığım yazıların tüm bilgisi    
    fields = models.CharField(choices = Fields.fields ,max_length=5,verbose_name ="Bölüm seçin") # konu belirleme yanı bu yazı yazılımlamı ilgili elektriklemi , bu sayede ilgili yere gidebilecek
    branch = models.CharField(choices = Branches.branches ,max_length=5,verbose_name = "Dal seçin")
    title = models.CharField(max_length=100,verbose_name = "Başlık yazın") # başlık bilgisi ama sadece admin de içiriğin ne oldugunu anlamak için yaptım
    url = models.SlugField(unique = True ,max_length=100,verbose_name = "Web adresi, başlık ile aynı olmasına özen gösterin ") # blogun url adresi 
    content = RichTextField(verbose_name = "içeriğinizi oluşturun")  # yazılan yazılar burda 
    tag = models.CharField(max_length=100,verbose_name = "İçeriğiniz ili ilgili anahtar kelimeleri virgul kullanarak yazın") # taglar konuyu ilgilendiren içeriği anlatan kısa isimler google aramalarında çıkması için
    time = models.DateTimeField(default=timezone.now) # tarih bilgisi 


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
    title =  models.CharField(max_length=50)# yazının başlık bilgisi
    time = models.DateTimeField(default=timezone.now) # tarih bilgisi 

