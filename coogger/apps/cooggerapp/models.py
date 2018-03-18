#django
from django.utils.text import slugify
from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from django.db.models import F
from django.urls import reverse

from social_django.models import AbstractUserSocialAuth, DjangoStorage, USER_MODEL

#django 3.
from ckeditor.fields import RichTextField

#choices
from apps.cooggerapp.choices import *

#python
from bs4 import BeautifulSoup
import random
import datetime

#steem
from steem.steem import Commit
from steem.post import Post
from steem.amount import Amount
from steem import Steem


class OtherInformationOfUsers(models.Model): # kullanıcıların diğer bilgileri
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    posting_key = models.CharField(max_length=250, verbose_name = "steemit posting key")
    about = RichTextField(null = True, blank = True,verbose_name = "kişi hakkında")
    hmanycontent = models.IntegerField(default = 0)


class Content(models.Model): # blog için yazdığım yazıların tüm bilgisi
    user = models.ForeignKey("auth.user" ,on_delete=models.CASCADE)
    content_list = models.CharField(default = "coogger",max_length=30,verbose_name ="Konu başlığınız",help_text = "İçeriğiniz belirli bir konu etrafında birden fazla olacak ise anlatacağınız konuyu yazın")
    title = models.CharField(max_length=100, verbose_name = "Başlık", help_text = "İçeriğiniz ile alakalı en güzel başlığı seçtiğinizden emin olun.")
    url = models.CharField(unique = True, max_length=200, verbose_name = "web adresi") # blogun url adresi
    content = RichTextField(verbose_name = "İçeriğinizi yazın")  # yazılan yazılar burda
    show = models.CharField(max_length=400, verbose_name = "İçeriğinizin tanımı",help_text = "Okuyucularınıza içerik hakkında kısaca bilgi verin.")
    tag = models.CharField(max_length=200, verbose_name = "Anahtar kelimeler",help_text = "anahtar kelimelerinizi virgül kullanarak yazın.") # taglar konuyu ilgilendiren içeriği anlatan kısa isimler google aramalarında çıkması için
    time = models.DateTimeField(default = timezone.now, verbose_name="tarih") # tarih bilgisi
    dor = models.CharField(default = 0, max_length=10)
    views = models.IntegerField(default = 0, verbose_name = "kişi görüntüledi")
    read = models.IntegerField(default = 0, verbose_name = "sayfa açılma sayısı")
    hmanycomment=models.IntegerField(default = 0, verbose_name = "yorum sayısı")
    lastmod = models.DateTimeField(default = timezone.now, verbose_name="son değiştirme tarihi")
    confirmation = models.BooleanField(default = False)

    class Meta:
        verbose_name = "content"
        ordering = ['-lastmod']

    def durationofread(self,text):
        reading_speed = 20 # 1 saniyede 20 harf okunursa
        read_content = BeautifulSoup(text, 'html.parser').get_text().replace(" ","")
        how_much_words = len(read_content)
        words_time = float((how_much_words/reading_speed)/60)
        return str(words_time)[:3]

    def content_save(self, *args, **kwargs):
        user = self.user
        list_ = slugify(self.content_list.lower(), allow_unicode=True)
        title = slugify(self.title.lower(), allow_unicode=True)
        tags = ""
        tag = self.tag.split(",")[:4]
        for i in tag:
            if i == tag[-1]:
                tags += slugify(i, allow_unicode=True)
            else:
                tags += slugify(i, allow_unicode=True)+" "
        tags = "deneme "+tags
        self.content_list = list_
        self.tag = tags
        self.dor = self.durationofread(self.content+self.title)
        self.url = str(user)+"/"+str(list_)+"/"+str(title)
        self.steemit_post(title = self.title, body = self.content, author = user, tags = tags)
        try:
            super(Content, self).save(*args, **kwargs)
        except:
            self.url = self.url + "-" +str(random.randrange(9999)) # TODO:  bu bölüm
            super(Content, self).update(*args, **kwargs)

    def content_update(self,queryset,content):
        user = queryset[0].user
        list_ = slugify(content.content_list.lower(), allow_unicode=True)
        title = slugify(content.title.lower(), allow_unicode=True)
        tags = ""
        tag = content.tag.split(",")[:4]
        for i in tag:
            if i == tag[-1]:
                tags += slugify(i, allow_unicode=True)
            else:
                tags += slugify(i, allow_unicode=True)+" "
        tags = "deneme "+tags
        dor = self.durationofread(content.content+content.title)
        if queryset[0].confirmation == True: # bu sayede her düzenleme yapıldıgında 1 azalmayacaktır.
            OtherInformationOfUsers.objects.filter(user = user).update(hmanycontent = F("hmanycontent") -1)
        self.steemit_edit_post(user,body = content.content, steemit_url = queryset[0].url.split("/"))
        queryset.update(lastmod = datetime.datetime.now(), show = content.show,title = content.title, content_list = list_, tag = tags, dor = dor, content = content.content, confirmation = False)
        return queryset[0].url

    def steemit_post(self, title, body, author, tags, reply_identifier = None):
        user_posting_key = OtherInformationOfUsers.objects.filter(user = author)[0].posting_key
        STEEM = Steem(keys = [str(user_posting_key)])
        Commit(steem = STEEM).post(
        title = title,
        body = body,
        author = str(author),
        permlink = None,
        reply_identifier = reply_identifier,
        json_metadata = None,
        comment_options = None,
        community = None,
        tags = tags,
        beneficiaries = None,
        self_vote = False
        )

    def steemit_edit_post(self, author, body, steemit_url):
        user_posting_key = OtherInformationOfUsers.objects.filter(user = author)[0].posting_key
        STEEM = Steem(keys = [str(user_posting_key)])
        Post(post = "@"+steemit_url[0]+"/"+steemit_url[2], steemd_instance = STEEM).edit(body = body)

    def get_steemit_url(self):
        s_url = self.url.split("/")
        return "@"+s_url[0]+"/"+s_url[2]

    def post_reward(self):
        post = Post(post = self.get_steemit_url())
        pp = self.pending_payout(post)
        sbd_sp = self.calculate_sbd_sp(pp)
        return dict(
        total = sbd_sp["total"],
        sbd = sbd_sp["sbd"],
        sp = sbd_sp["sp"]
        )

    def calculate_sbd_sp(self, payout):
        return dict(
        total = round(payout,4),
        sp = round(payout * 0.15,4),
        sbd = round(payout * 0.75/2,4),
        )

    def pending_payout(self, post):
        payout = Amount(post.pending_payout_value).amount
        if payout == 0:
            payout = (Amount(post.total_payout_value).amount + Amount(post.curator_payout_value).amount)
        return payout


class UserFollow(models.Model):
    user = models.ForeignKey("auth.user" ,on_delete=models.CASCADE)
    choices = models.CharField(max_length=15, choices = make_choices(follow()),verbose_name="Web sitesi")
    adress = models.CharField(max_length=150, verbose_name = "Adresi yazın")


class Following(models.Model):
    user = models.ForeignKey("auth.user" ,on_delete=models.CASCADE)
    which_user = models.ForeignKey("auth.user" ,on_delete=models.CASCADE, related_name='%(class)s_requests_created')


class Comment(models.Model):
    user = models.ForeignKey("auth.user", on_delete=models.CASCADE ,verbose_name="yorum yapan kişi")
    content = models.ForeignKey("content" ,on_delete=models.CASCADE)
    date = models.DateTimeField(default = timezone.now,verbose_name="tarih")
    comment = models.CharField(max_length=310,verbose_name="Soru sor veya teşekkür et, yorum yap")

    # def steemit_post(self, title, body, author, tags, reply_identifier = None):
    #     user_posting_key = OtherInformationOfUsers.objects.filter(user = author)[0].posting_key
    #     STEEM = Steem(keys = [str(user_posting_key)])
    #     Commit(steem = STEEM).post(
    #     title = title,
    #     body = body,
    #     author = str(author),
    #     permlink = None,
    #     reply_identifier = reply_identifier,
    #     json_metadata = None,
    #     comment_options = None,
    #     community = None,
    #     tags = tags,
    #     beneficiaries = None,
    #     self_vote = False
    #     )


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

    def save(self, *args, **kwargs):
        try:
            super(SearchedWords, self).save(*args, **kwargs)
        except:
            SearchedWords.objects.filter(word = self.word).update(hmany = F("hmany") + 1)


class Report(models.Model):
    choices_reports = make_choices(reports())
    user = models.ForeignKey("auth.user" ,on_delete=models.CASCADE,verbose_name = "şikayet eden kişi")
    content = models.ForeignKey("content" ,on_delete=models.CASCADE,verbose_name = "şikayet edilen içerik")
    complaints = models.CharField(choices = choices_reports,max_length=40,verbose_name="şikayet türleri")
    add = models.CharField(blank = True,null = True, max_length = 600,verbose_name = "Daha fazla bilgi vermek istermisin ?")
    date = models.DateTimeField(default = timezone.now)


class Contentviews(models.Model):
    content = models.ForeignKey(Content ,on_delete=models.CASCADE)
    ip = models.GenericIPAddressField()
