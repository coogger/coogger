#django
from django.utils.text import slugify
from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone

from social_django.models import UserSocialAuth
from social_django.models import AbstractUserSocialAuth, DjangoStorage, USER_MODEL

#choices
from cooggerapp.choices import *

#python
import random
import datetime

#steem
from steem.post import Post

# sc2py.
from sc2py.sc2py import Sc2
from sc2py.operations import Operations
from sc2py.operations import Comment_options
from sc2py.operations import Comment
from sc2py.operations import Follow
from sc2py.operations import Unfollow

# 3. other
from bs4 import BeautifulSoup
import mistune


from djmd.models import EditorMdField

class OtherInformationOfUsers(models.Model): # kullanıcıların diğer bilgileri
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    about = EditorMdField()
    hmanycontent = models.IntegerField(default = 0)
    cooggerup_confirmation = models.BooleanField(default = False, verbose_name = "Do you want to join in curation trails of the cooggerup bot with your account?")
    cooggerup_percent = models.CharField(max_length = 3,choices = make_choices([i for i in range(100,-1,-1)]),default = 0)
    vote_percent = models.CharField(max_length = 3,choices = make_choices([i for i in range(100,0,-1)]),default = 100)
    beneficiaries = models.CharField(max_length = 3,choices = make_choices([i for i in range(100,-1,-1)]),default = 0)

    def s_info(self):
        return UserSocialAuth.objects.filter(uid = self.user)[0].extra_data

    def get_access_token(self):
        return self.s_info()["access_token"]

class Content(models.Model):
    user = models.ForeignKey("auth.user" ,on_delete=models.CASCADE)
    title = models.CharField(max_length=100, verbose_name = "Title", help_text = "Be sure to choose the best title related to your content.")
    permlink = models.SlugField(max_length=200)
    content = EditorMdField()
    tag = models.CharField(max_length=200, verbose_name = "keyword",help_text = "Write your tags using spaces,the first tag is your topic max:4 .") # taglar konuyu ilgilendiren içeriği anlatan kısa isimler google aramalarında çıkması için
    category = models.CharField(max_length=30,choices = make_choices(category_choices()) ,help_text = "select content category")
    language = models.CharField(max_length=30,choices = make_choices(lang_choices()) ,help_text = "The language of your content")
    definition = models.CharField(max_length=400, verbose_name = "definition of content",help_text = "Briefly tell your readers about your content.")
    topic = models.CharField(max_length=30,verbose_name ="content topic",help_text = "Please, write your topic about your contents.")

    status = models.CharField(max_length=30,choices = make_choices(status_choices()) ,verbose_name = "content's status")
    time = models.DateTimeField(default = timezone.now, verbose_name="date") # tarih bilgisi
    dor = models.CharField(default = 0, max_length=10)
    views = models.IntegerField(default = 0, verbose_name = "views")
    read = models.IntegerField(default = 0, verbose_name = "pageviews")
    lastmod = models.DateTimeField(default = timezone.now, verbose_name="last modified date")

    mod = models.ForeignKey("auth.user",on_delete=models.CASCADE,blank = True,null = True, related_name="moderator") # inceleyen mod bilgisi
    cooggerup = models.BooleanField(default = False,verbose_name = "was voting done")

    @property
    def username(self):
        return self.user.username

    @property
    def modusername(self):
        return self.mod.username

    class Meta:
        ordering = ['-time']

    def misdef(self):
        renderer = mistune.Renderer(escape=False)
        markdown = mistune.Markdown(renderer=renderer)
        return markdown(self.definition)

    @staticmethod
    def prepare_definition(text): # TODO:  zaten alınan ilk 400 karakterde resim varsa ikinci bir resmi almaması gerek
        renderer = mistune.Renderer(escape=False)
        markdown = mistune.Markdown(renderer=renderer)
        beautifultext = BeautifulSoup(markdown(text),"html.parser")
        try:# if the first 400 characters are in the image
            src = beautifultext[0:400].find("img").get("src")
            alt = beautifultext[0:400].find("img").get("alt")
            image_markdown = "![{}]({})".format(alt,src)
            return beautifultext.text[0:400-len(image_markdown)-4]+"..."
        except: # if the first 400 characters are not in the image
            try:
                src = beautifultext.find("img").get("src")
                alt = beautifultext.find("img").get("alt")
                image_markdown = "![{}]({})".format(alt,src)
                return beautifultext.text[0:400-len(image_markdown)-4]+"..."+image_markdown
            except: # if there isn't image in content
                return  beautifultext.text[0:400-4]+"..."

    def get_absolute_url(self):
        return "@"+self.user.username+"/"+self.permlink

    @staticmethod
    def durationofread(text):
        reading_speed = 20 # 1 saniyede 20 harf okunursa
        read_content = BeautifulSoup(text, 'html.parser').get_text().replace(" ","")
        how_much_words = len(read_content)
        words_time = float((how_much_words/reading_speed)/60)
        return str(words_time)[:3]

    def save(self, *args, **kwargs): # for admin.py
        self.definition = self.prepare_definition(self.content)
        super(Content, self).save(*args, **kwargs)

    def content_save(self, *args, **kwargs): # for me
        self.tag = self.ready_tags()
        self.topic = self.tag.split()[1]
        self.dor = self.durationofread(self.content+self.title)
        self.permlink = slugify(self.title.lower())
        self.definition = self.prepare_definition(self.content)
        while  True: # hem coogger'da hemde sistem'de olmaması gerek ki kayıt sırasında sorun çıkmasın.
            try: # TODO:  buralarda sorun var aynı adres steemit de yokken coogger'da vardı ve döngüden çıkamadı.
                Content.objects.filter(user = self.user,permlink = self.permlink)[0] # db de varsa
                try:
                    Post(post = self.get_absolute_url()).url # sistem'de varsa
                    self.new_permlink() # change to self.permlink / link değişir
                except:
                    pass
            except:
                try:
                    Post(post = self.get_absolute_url()).url # sistem'de varsa
                    self.new_permlink() # change to self.permlink / link değişir
                except:
                    break
        steem_save = self.sc2_post(self.permlink, "save")
        if steem_save.status_code == 200:
            super(Content, self).save(*args, **kwargs)
            return steem_save
        return steem_save

    def content_update(self,queryset,content):
        self.user = queryset[0].user
        self.title = content.title
        self.permlink = queryset[0].permlink # no change
        self.status = queryset[0].status # düzenlemeni onay almaya ihtiyacı varmı diye
        # daha sonradan değiştirilebilir.
        self.tag = self.ready_tags()
        self.topic = self.tag.split()[1]
        self.dor = self.durationofread(self.content+self.title)
        queryset.update(definition = self.prepare_definition(content.content),
        topic = self.topic,
        permlink = self.permlink,
        title = self.title,
        content = self.content,
        tag = self.tag,
        dor = self.dor,
        status = self.status,
        lastmod = datetime.datetime.now(),
        )
        return self.sc2_post(self.permlink, "update")

    def sc2_post(self,permlink,json_metadata):
        def_name = json_metadata
        if json_metadata == "update" or json_metadata == "save":
            json_metadata = {
            "format":"markdown",
            "tags":self.ready_tags().split(),
            "app":"coogger/1.3.0",
            "community":"coogger",
            "content":{"status":self.status,"dor":self.dor,"topic":self.topic},
            }
        ms = """\n\n----------
        \nPosted on [coogger.com](http://www.coogger.com/{}) - The first platform to reward information sharing
        \n----------""".format(self.get_absolute_url())
        comment = Comment(
        parent_permlink = "coogger",
        author = str(self.user.username),
        permlink = permlink,
        title = self.title,
        body = self.content + ms,
        json_metadata = json_metadata,
        )
        if def_name == "save":
            beneficiaries_weight = OtherInformationOfUsers.objects.filter(user = self.user)[0].beneficiaries
            if int(beneficiaries_weight) != 0:
                comment_options = Comment_options(
                author = str(self.user.username),
                permlink = permlink,
                beneficiaries = {"account":"coogger","weight":int(beneficiaries_weight) * 100}
                )
                jsons = comment.json+comment_options.json
            else:
                jsons = comment.json
        else:
            jsons = comment.json
        op = Operations(json = jsons).json
        access_token = OtherInformationOfUsers(user = self.user).get_access_token()
        return Sc2(token = access_token,data = op).run

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
        return clearly_tags(get_tag)

    def new_permlink(self):
        rand = str(random.randrange(9999))
        self.permlink += "-"+rand


class UserFollow(models.Model):
    user = models.ForeignKey("auth.user" ,on_delete=models.CASCADE)
    choices = models.CharField(blank = True,null = True,max_length=15, choices = make_choices(follow()),verbose_name="website")
    adress = models.CharField(blank = True,null = True,max_length=150, verbose_name = "write address / username")

class SearchedWords(models.Model):
    word = models.CharField(unique=True,max_length=310)
    hmany = models.IntegerField(default = 1)

    def save(self, *args, **kwargs):
        try:
            super(SearchedWords, self).save(*args, **kwargs)
        except:
            SearchedWords.objects.filter(word = self.word).update(hmany = models.F("hmany") + 1)

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

class CustomUserSocialAuth(AbstractUserSocialAuth): # bu kısmı kendine göre ayarla.
    user = models.ForeignKey(USER_MODEL, related_name='custom_social_auth',on_delete=models.CASCADE)

class CustomDjangoStorage(DjangoStorage):
    user = CustomUserSocialAuth
