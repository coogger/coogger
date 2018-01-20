from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from ckeditor.fields import RichTextField
from cooggerapp.choices import *
from django.utils.text import slugify
from bs4 import BeautifulSoup

class Content(models.Model): # blog için yazdığım yazıların tüm bilgisi
    user = models.ForeignKey("auth.user" ,on_delete=models.CASCADE)
    content_list = models.SlugField(null = True, blank = True, default="coogger", max_length=30, verbose_name ="Liste ismi")
    title = models.CharField(max_length=100, verbose_name = "Başlık") # başlık bilgisi ama sadece admin de içiriğin ne oldugunu anlamak için yaptım
    url = models.CharField(unique = True, max_length=200, verbose_name = "web adresi") # blogun url adresi
    content = RichTextField(verbose_name = "İçeriğinizi yazın")  # yazılan yazılar burda
    show = models.CharField(max_length=400, verbose_name = "İçeriğinizin tanımı")
    tag = models.CharField(max_length=200, verbose_name = "Anahtar kelimeler") # taglar konuyu ilgilendiren içeriği anlatan kısa isimler google aramalarında çıkması için
    time = models.DateTimeField(default = timezone.now, verbose_name="tarih") # tarih bilgisi
    dor = models.CharField(default = 0, max_length=10, verbose_name = "duration of read")
    views = models.IntegerField(default = 0, verbose_name = "görüntülenme sayısı") # görütülenme sayısını kayıt eder
    hmanycomment=models.IntegerField(default = 0, verbose_name = "yorum sayısı")
    lastmod = models.DateTimeField(default = timezone.now, verbose_name="son değiştirme tarihi")
    confirmation = models.BooleanField(default = False)
    class Meta:
        verbose_name = "content"
        ordering = ['-time']

    def durationofread(self,text):
        reading_speed = 20 # 1 saniyede 20 harf okunursa
        read_content = BeautifulSoup(text, 'html.parser').get_text().replace(" ","")
        how_much_words = len(read_content)
        words_time = float((how_much_words/reading_speed)/60)
        return str(words_time)[:3]

    def save(self, *args, **kwargs):
        user = self.user
        list_ = slugify(self.content_list.lower(), allow_unicode=True)
        title = slugify(self.title.lower(), allow_unicode=True)
        url = str(user)+"/"+str(list_)+"/"+str(title)
        tags = ""
        tag = self.tag.split(",")
        for i in tag:
            if i == tag[-1]:
                tags += slugify(i, allow_unicode=True)
            else:
                tags += slugify(i, allow_unicode=True)+","
        self.url = url
        self.content_list = list_
        self.tag  = tags
        self.dor = self.durationofread(self.content+self.title)
        super(Content, self).save(*args, **kwargs)


class Following(models.Model):
    user = models.ForeignKey("auth.user" ,on_delete=models.CASCADE)
    which_user = models.ForeignKey("auth.user" ,on_delete=models.CASCADE, related_name='%(class)s_requests_created')


class Contentviews(models.Model): # görüntülenme ip ve blog_id bilgisini kayıt eder
    content = models.ForeignKey("content" ,on_delete=models.CASCADE)
    ip = models.GenericIPAddressField()


class ContentList(models.Model): # kullanıcıların sahip oldukları listeler
    user = models.ForeignKey("auth.user" ,on_delete=models.CASCADE)
    content_list = models.SlugField(max_length=30,verbose_name ="İçerik listeniz")
    content_count = models.IntegerField(verbose_name = "liste içindeki nesne sayısı")


class OtherInformationOfUsers(models.Model): # kullanıcıların diğer bilgileri
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    pp = models.BooleanField(default = False,verbose_name = "profil resmi") # profil resmi yüklemişmi
    is_author = models.BooleanField(default = True, verbose_name = "yazar olarak kabul et") # onaylanıp onaylanmadıgı
    author = models.BooleanField(default = True, verbose_name = "yazarlık başvurusu") # yazar başvurusu yaptımı ?
    about = RichTextField(null = True, blank = True,verbose_name = "kişi hakkında")
    following = models.IntegerField(default = 0)
    followers = models.IntegerField(default = 0)


class Author(models.Model): # yazarlık bilgileri
    choices_sex = (
        ("male","erkek"),
        ("female","kadın"),
    )
    choices_country = make_choices(country())
    old = [i for i in range(1905,2017)]
    choices_old = make_choices(old)
    choices_university = make_choices(university())
    choices_jop = make_choices(jop())
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    sex = models.CharField(choices = choices_sex,max_length=6,verbose_name="cinsiyet")
    county = models.CharField(choices = choices_country,max_length=50,verbose_name="memleket")
    old = models.CharField(choices = choices_old,verbose_name="doğum tarihin",max_length=4)
    university = models.CharField(null=True,choices = choices_university,verbose_name="üniversite",max_length=100)
    jop = models.CharField(null=True,choices = choices_jop,verbose_name="meslek",max_length=30) # boş olamaz uni yazmamış ise öğrenci olarak seçer
    phone = models.IntegerField(blank=True, null=True,unique = True,verbose_name = "telefon numarası")

    def save(self,*args,**kwargs):
        OtherInformationOfUsers.objects.filter(user = self.user).update(author = True)
        super(Author,self).save(*args,**kwargs)


class UserFollow(models.Model):
    user = models.ForeignKey("auth.user" ,on_delete=models.CASCADE)
    choices = models.CharField(max_length=15, choices = make_choices(follow()),verbose_name="Web sitesi")
    adress = models.CharField(max_length=150, verbose_name = "Adresi yazın")


class Comment(models.Model):
    user = models.ForeignKey("auth.user", on_delete=models.CASCADE ,verbose_name="yorum yapan kişi")
    content = models.ForeignKey("content" ,on_delete=models.CASCADE)
    date = models.DateTimeField(default = timezone.now,verbose_name="tarih")
    comment = models.CharField(max_length=310,verbose_name="Soru sor veya teşekkür et, yorum yap")


class Notification(models.Model):
    user = models.ForeignKey("auth.user", on_delete=models.CASCADE, verbose_name="bildirimin gittiği kişi")
    even = models.IntegerField(verbose_name="bildirime sebeb olan olay numarası")
    content = models.CharField(max_length=310,verbose_name="bildirim mesajı")
    show = models.BooleanField(default=False,verbose_name="gördü/görmedi")
    address = models.SlugField(verbose_name="bildirimin gerçekleştiği adres")
    time = models.DateTimeField(default = timezone.now,verbose_name="tarih")


class SearchedWords(models.Model):
    word = models.CharField(unique=True,max_length=310)
    hmany = models.IntegerField(default = 1)
