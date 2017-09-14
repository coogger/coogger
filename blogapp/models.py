from django.db import models
from django.utils import timezone
from ckeditor.fields import RichTextField 

class Content(models.Model): # blog için yazdığım yazıların tüm bilgisi
    SOFTWARE = "SW"
    ELECTRICITY_AND_ELECTRONICS = "EAE"
    SELECT_İSSUE = (
        (SOFTWARE, 'software'),
        (ELECTRICITY_AND_ELECTRONICS, 'electriciy and electronics'),
    )
    username = models.ForeignKey("auth.User")
    issue = models.CharField(choices = SELECT_İSSUE, default=SOFTWARE ,max_length=100) # konu belirleme yanı bu yazı yazılımlamı ilgili elektriklemi , bu sayede ilgili yere gidebilecek
    title = models.CharField(max_length=100) # başlık bilgisi ama sadece admin de içiriğin ne oldugunu anlamak için yaptım
    url = models.SlugField(unique = True ,max_length=100) # blogun url adresi 
    tag = models.CharField(max_length=100) # taglar konuyu ilgilendiren içeriği anlatan kısa isimler google aramalarında çıkması için
    content = RichTextField()  # yazılan yazılar burda 
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


