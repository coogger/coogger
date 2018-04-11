#django
from django.utils.text import slugify
from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from django.db.models import F

from social_django.models import UserSocialAuth
from social_django.models import AbstractUserSocialAuth, DjangoStorage, USER_MODEL
from martor.models import MartorField

#choices
from apps.cooggerapp.choices import *

#python
from bs4 import BeautifulSoup
import random
import datetime

#steem
from steem.post import Post
from steem.amount import Amount

# 3.
from sc2py.sc2py import Sc2

class OtherInformationOfUsers(models.Model): # kullanıcıların diğer bilgileri
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    about = MartorField()
    follower_count = models.IntegerField(default = 0)
    following_count = models.IntegerField(default = 0)
    hmanycontent = models.IntegerField(default = 0)
    cooggerup_confirmation = models.BooleanField(default = False, verbose_name = "Do you want to join in curation trails of the cooggerup bot with your account?")
    percents = [i for i in range(100,0,-1)]
    cooggerup_percent = models.CharField(max_length = 3,choices = make_choices(percents),default = 0)

    def s_info(self):
        return UserSocialAuth.objects.filter(uid = self.user)[0].extra_data

class Content(models.Model):
    user = models.ForeignKey("auth.user" ,on_delete=models.CASCADE)
    content_list = models.CharField(default = "coogger",max_length=30,verbose_name ="title of list",help_text = "If your contents will continue around a particular topic, write your topic it down.")
    permlink = models.CharField(unique = True, max_length=200, verbose_name = "permlink") # blogun url adresi
    title = models.CharField(max_length=100, verbose_name = "Title", help_text = "Be sure to choose the best title related to your content.")
    definition = models.CharField(max_length=400, verbose_name = "definition of content",help_text = "Briefly tell your readers about your content.")
    content = MartorField()
    tag = models.CharField(max_length=200, verbose_name = "keyword",help_text = "Write your keywords using spaces max:4 .") # taglar konuyu ilgilendiren içeriği anlatan kısa isimler google aramalarında çıkması için
    time = models.DateTimeField(default = timezone.now, verbose_name="date") # tarih bilgisi
    dor = models.CharField(default = 0, max_length=10)
    views = models.IntegerField(default = 0, verbose_name = "views")
    read = models.IntegerField(default = 0, verbose_name = "pageviews")
    hmanycomment=models.IntegerField(default = 0, verbose_name = "comments count")
    lastmod = models.DateTimeField(default = timezone.now, verbose_name="last modified date")
    draft = models.BooleanField(default = False,verbose_name = "content draft")
    # ------------ #
    cantapproved = models.CharField(max_length=40,choices = make_choices(cantapproved_choices()) ,verbose_name = "Why can not approved")
    cooggerup = models.BooleanField(default = False,verbose_name = "upvote with cooggerup bot")
    upvote = models.BooleanField(default = False,verbose_name = "was voting done")

    class Meta:
        verbose_name = "content"
        ordering = ['-time']

    def get_absolute_url(self):
        return "@"+self.user.username+"/"+self.content_list+"/"+self.permlink

    @staticmethod
    def durationofread(text):
        reading_speed = 20 # 1 saniyede 20 harf okunursa
        read_content = BeautifulSoup(text, 'html.parser').get_text().replace(" ","")
        how_much_words = len(read_content)
        words_time = float((how_much_words/reading_speed)/60)
        return str(words_time)[:3]

    def content_save(self, *args, **kwargs):
        self.content_list = slugify(self.content_list.lower())
        self.tag = self.ready_tags()["coogger"]
        self.dor = self.durationofread(self.content+self.title)
        self.permlink = slugify(self.title.lower())
        try:
            Post(post = self.get_steemit_url()).url
            rand = str(random.randrange(9999))
            self.permlink += "-"+rand
        except:
            pass
        if self.sc2_post(self.permlink).status_code == 200:
            self.draft = False
        else:
            self.draft = True
        super(Content, self).save(*args, **kwargs)

    def content_update(self,queryset,content):
        self.user = queryset[0].user
        self.show = content.show
        self.content_list = slugify(content.content_list.lower())
        self.content = content.content
        self.title = content.title # no change
        self.permlink = slugify(queryset[0].title.lower()) # no change
        self.tag = content.tag
        self.draft = queryset[0].draft
        self.tag = self.ready_tags()["coogger"]
        self.dor = self.durationofread(self.content+self.title)
        if self.draft:
            try:
                Post(post = self.get_steemit_url()).url
                rand = str(random.randrange(9999))
                self.permlink += "-"+rand
            except:
                pass
            if self.sc2_post(self.permlink).status_code == 200:
                self.draft = False
            else:
                self.draft = True
        queryset.update(show = self.show,
        content_list = self.content_list,
        permlink = self.permlink,
        title = self.title,
        content = self.content,
        tag = self.tag,
        draft = self.draft,
        dor = self.dor,
        lastmod = datetime.datetime.now(),
        )
        return "@"+self.user.username+"/"+self.content_list+"/"+self.permlink

    def sc2_post(self,permlink):
        access_token = UserSocialAuth.objects.filter(uid = self.user)[0].extra_data["access_token"]
        sum_of_post = """\n\n----------
        \nPosted on  [coogger.com](http://www.coogger.com/{})  - The platform that rewards information sharing
        \n ----------""".format(self.get_absolute_url())
        content = self.content + sum_of_post
        return Sc2(str(access_token)).post(str(self.user.username),str(self.title),str(content),self.ready_tags()["steemit"],permlink)

    def ready_tags(self):
        def clearly_tags(get_tag):
            clearly_tags = []
            tags = ""
            for i in get_tag:
                if i not in clearly_tags:
                    clearly_tags.append(i)
            for i in clearly_tags:
                if i == clearly_tags[-1]:
                    tags += slugify(i.lower())
                else:
                    tags += slugify(i.lower())+" "
            return tags
        get_tag = self.tag.split(" ")[:4]
        if get_tag[0] != "coogger":
            get_tag.insert(0,"coogger")
        return {"steemit":clearly_tags(get_tag),"coogger":clearly_tags(self.tag.split(" ")[:5])}

    def get_steemit_url(self):
        s_url = self.get_absolute_url().split("/")
        return s_url[0]+"/"+s_url[2]

    def get_steemit_permlink(self):
        return self.permlink

    def post_reward(self):
        try:
            post = Post(post = self.get_steemit_url())
            pp = self.pending_payout(post)
            sbd_sp = self.calculate_sbd_sp(pp)
            return dict(total = sbd_sp["total"])
        except:
            return dict(total = None,)

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
    choices = models.CharField(max_length=15, choices = make_choices(follow()),verbose_name="website")
    adress = models.CharField(max_length=150, verbose_name = "write address / username")

class Following(models.Model):
    user = models.ForeignKey("auth.user" ,on_delete=models.CASCADE)
    which_user = models.ForeignKey("auth.user" ,on_delete=models.CASCADE, related_name='%(class)s_requests_created')

class SearchedWords(models.Model):
    word = models.CharField(unique=True,max_length=310)
    hmany = models.IntegerField(default = 1)

    def save(self, *args, **kwargs):
        try:
            super(SearchedWords, self).save(*args, **kwargs)
        except:
            SearchedWords.objects.filter(word = self.word).update(hmany = F("hmany") + 1)

class ReportModel(models.Model):
    choices_reports = make_choices(reports())
    user = models.ForeignKey("auth.user" ,on_delete=models.CASCADE,verbose_name = "şikayet eden kişi")
    content = models.ForeignKey("content" ,on_delete=models.CASCADE,verbose_name = "şikayet edilen içerik")
    complaints = models.CharField(choices = choices_reports,max_length=40,verbose_name="type of report")
    add = models.CharField(blank = True,null = True, max_length = 600,verbose_name = "Can you give more information ?")
    date = models.DateTimeField(default = timezone.now)

class Contentviews(models.Model):
    content = models.ForeignKey(Content ,on_delete=models.CASCADE)
    ip = models.GenericIPAddressField()

class CustomUserSocialAuth(AbstractUserSocialAuth):
    user = models.ForeignKey(USER_MODEL, related_name='custom_social_auth',on_delete=models.CASCADE)

class CustomDjangoStorage(DjangoStorage):
    user = CustomUserSocialAuth
