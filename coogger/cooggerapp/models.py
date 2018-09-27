# django
from django.utils.text import slugify
from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone

# choices
from cooggerapp.choices import *

# python
import random
import datetime

# steem
from steem.post import Post

# steemconnect
from steemconnect.steemconnect import SteemConnect
from steemconnect.operations import (
    Unfollow, Comment,
    Follow, Unfollow, CommentOptions
)

# 3. other
from bs4 import BeautifulSoup
import mistune

from django_md_editor.models import EditorMdField
from django_steemconnect.models import SteemConnectUser, Community


class EditorTemplate(models.Model):
    category_name = models.CharField(max_length=100, unique=True, verbose_name="Category name")
    template = EditorMdField()


class OtherInformationOfUsers(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    about = EditorMdField()
    cooggerup_confirmation = models.BooleanField(default=False, verbose_name="Do you want to join in curation trails of the cooggerup bot with your account?")
    sponsor = models.BooleanField(default=False)
    cooggerup_percent = models.FloatField(default=0, verbose_name="Cooggerup bot upvote percent")
    vote_percent = models.FloatField(default=100)
    beneficiaries = models.FloatField(default=0, verbose_name="Support Coogger ecosystem with beneficiaries")
    # reward db of coogger.up curation trail, reset per week
    total_votes = models.IntegerField(default=0, verbose_name="How many votes")
    total_vote_value = models.FloatField(default=0, verbose_name="total vote value")

    @property
    def username(self):
        return self.user.username


class Content(models.Model):
    community = models.ForeignKey(Community, on_delete=models.CASCADE)
    user = models.ForeignKey("auth.user", on_delete=models.CASCADE)
    title = models.CharField(max_length=200, verbose_name="Title", help_text="Be sure to choose the best title related to your content.")
    permlink = models.SlugField(max_length=200)
    content = EditorMdField()
    tag = models.CharField(max_length=200, verbose_name="keyword", help_text="Write your tags using spaces, max:4")
    language = models.CharField(max_length=30, choices=make_choices(languages), help_text=" The language of your content")
    category = models.CharField(max_length=30, choices=make_choices(all_categories), help_text="select content category")
    definition = models.CharField(max_length=400, verbose_name="definition of content", help_text="Briefly tell your readers about your content.")
    topic = models.CharField(max_length=30, verbose_name="content topic", help_text="Please, write your topic about your contents.")
    status = models.CharField(default="shared", max_length=30, choices=make_choices(status_choices), verbose_name="content's status")
    time = models.DateTimeField(default=timezone.now, verbose_name="date")
    dor = models.CharField(default=0, max_length=10)
    views = models.IntegerField(default=0, verbose_name="views")
    read = models.IntegerField(default=0, verbose_name="pageviews")
    lastmod = models.DateTimeField(default=timezone.now, verbose_name="last modified date")
    mod = models.ForeignKey("auth.user", on_delete=models.CASCADE, blank=True, null=True, related_name="moderator")
    cooggerup = models.BooleanField(default=False, verbose_name="was voting done")

    class Meta:
        ordering = ['-time']

    @property
    def username(self):
        return self.user.username

    @property
    def modusername(self):
        return self.mod.username

    @property
    def community_name(self):
        return self.community.name

    @staticmethod
    def prepare_definition(text):
        renderer = mistune.Renderer(escape=False, parse_block_html=True)
        markdown = mistune.Markdown(renderer=renderer)
        soup = BeautifulSoup(markdown(text), "html.parser")
        img = soup.find("img")
        if img is None:
            return "<p>{}</p>".format(soup.text[0:200]+"...")
        src = img.get("src")
        try:
            alt = img.get("alt")
        except:
            alt = ""
        return "<img class='definition-img' src='{}' alt='{}'></img><p>{}</p>".format(src, alt, soup.text[0:200]+"...")

    def get_absolute_url(self):
        return "@"+self.user.username+"/"+self.permlink

    @staticmethod
    def durationofread(text):
        reading_speed = 20  # 1 saniyede 20 harf okunursa
        read_content = BeautifulSoup(text, 'html.parser').get_text().replace(" ", "")
        how_much_words = len(read_content)
        words_time = float((how_much_words/reading_speed)/60)
        return str(words_time)[:3]

    def save(self, *args, **kwargs):  # for admin.py
        if self.mod == User.objects.get(username="hakancelik"):
            try:
                POST = Post(post=f"@{self.user}/{self.permlink}")
                self.steemconnect_post(self.permlink, "update")
            except:
                steem_post = self.steemconnect_post(self.permlink, "save")
        self.definition = self.prepare_definition(self.content)
        super(Content, self).save(*args, **kwargs)

    def content_save(self, request, *args, **kwargs):  # for me
        self.community = request.community_model
        self.tag = self.ready_tags()
        self.dor = self.durationofread(self.content+self.title)
        self.permlink = slugify(self.title.lower())
        self.definition = self.prepare_definition(self.content)
        while True:  # hem coogger'da hemde sistem'de olmaması gerek ki kayıt sırasında sorun çıkmasın.
            try:  # TODO:  buralarda sorun var aynı adres steemit de yokken coogger'da vardı ve döngüden çıkamadı.
                Content.objects.filter(user=self.user, permlink=self.permlink)[0]  # db de varsa
                try:
                    Post(post=self.get_absolute_url()).url  # sistem'de varsa
                    self.new_permlink()  # change to self.permlink / link değişir
                except:
                    pass
            except:
                try:
                    Post(post=self.get_absolute_url()).url  # sistem'de varsa
                    self.new_permlink()  # change to self.permlink / link değişir
                except:
                    break
        steem_save = self.steemconnect_post(self.permlink, "save")
        if steem_save.status_code == 200:
            super(Content, self).save(*args, **kwargs)
        return steem_save

    def content_update(self, queryset, content):
        self.community = queryset[0].community
        self.user = queryset[0].user
        self.title = content.title
        self.tag = self.ready_tags(limit=5)
        self.topic = content.topic
        self.dor = self.durationofread(self.content+self.title)
        steem_post = self.steemconnect_post(queryset[0].permlink, "update")
        if steem_post.status_code == 200:
            queryset.update(
                definition=self.prepare_definition(content.content),
                topic=self.topic,
                title=self.title,
                content=self.content,
                category=content.category,
                language=content.language,
                tag=self.tag,
                status="changed",
                dor=self.dor,
                lastmod=timezone.now(),
            )
        return steem_post

    def steemconnect_post(self, permlink, json_metadata):
        def_name = json_metadata
        if json_metadata == "save":
            self.content += "\n"+self.community.ms.format(self.get_absolute_url())
        json_metadata = {
            "format": "markdown",
            "tags": self.tag.split(),
            "app": "coogger/1.3.9",
            "ecosystem": "coogger",
            "community": self.community.name,
            "topic": self.topic,
            "category": self.category,
            "language": self.language,
            "dor": self.dor,
        }
        comment = Comment(
            parent_author = "",
            parent_permlink=self.community.name,
            author=str(self.user.username),
            permlink=permlink,
            title=self.title,
            body=self.content,
            json_metadata=json_metadata,
        )
        if def_name == "save":
            beneficiaries_weight = OtherInformationOfUsers.objects.filter(user=self.user)[0].beneficiaries
            beneficiaries_weight = round(float(beneficiaries_weight),3)
            if beneficiaries_weight >= 15:
                ben_weight = beneficiaries_weight * 100 - 1000
                if self.community.name == "coogger":
                    beneficiaries = [
                        {"account": "hakancelik", "weight": ben_weight + 1000},
                        ]
                else:
                    beneficiaries = [
                        {"account": "hakancelik", "weight": ben_weight+500},
                        {"account": self.community.name, "weight": 500}
                        ]
                comment_options = CommentOptions(parent_comment=comment, beneficiaries=beneficiaries)
                operation = comment_options.operation
            elif beneficiaries_weight < 15 and beneficiaries_weight > 0:
                ben_weight = beneficiaries_weight * 100 / 3
                if self.community.name == "coogger":
                    beneficiaries = [
                        {"account": "hakancelik", "weight": 3 * ben_weight },
                        ]
                else:
                    beneficiaries = [
                        {"account": "hakancelik", "weight": 2 * ben_weight},
                        {"account": self.community.name, "weight": ben_weight}
                        ]
                comment_options = CommentOptions(parent_comment=comment, beneficiaries=beneficiaries)
                operation = comment_options.operation
            else:
                operation = comment.operation
        else:
            operation = comment.operation
        steem_connect_user = SteemConnectUser.objects.filter(user=self.user)
        try:
            access_token = steem_connect_user[0].access_token
            return SteemConnect(token=access_token, data=operation).run
        except:
            sc_community_name = steem_connect_user[0].community_name
            secret = Community.objects.filter(name=sc_community_name)[0].app_secret
            access_token = steem_connect_user.set_new_access_token(secret)
            return SteemConnect(token=access_token, data=operation).run

    def ready_tags(self, limit=5):
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
        get_tag = self.tag.split(" ")[:limit]
        get_tag.insert(0, self.community.name)
        return clearly_tags(get_tag)

    def new_permlink(self):
        rand = str(random.randrange(9999))
        self.permlink += "-"+rand


class UserFollow(models.Model):
    user = models.ForeignKey("auth.user", on_delete=models.CASCADE)
    choices = models.CharField(blank=True, null=True, max_length=15, choices=make_choices(follow), verbose_name="website")
    adress = models.CharField(blank=True, null=True, max_length=150, verbose_name="write address / username")

    @property
    def username(self):
        return self.user.username


class SearchedWords(models.Model):
    # TODO:  add new column named user, as user or None
    word = models.CharField(unique=True, max_length=310)
    hmany = models.IntegerField(default=1)

    def save(self, *args, **kwargs):
        try:
            super(SearchedWords, self).save(*args, **kwargs)
        except:
            SearchedWords.objects.filter(word=self.word).update(hmany=models.F("hmany") + 1)


class ReportModel(models.Model):
    user = models.ForeignKey("auth.user", on_delete=models.CASCADE, verbose_name="şikayet eden kişi")
    content = models.ForeignKey("content", on_delete=models.CASCADE, verbose_name="şikayet edilen içerik")
    complaints = models.CharField(choices=make_choices(reports), max_length=40, verbose_name="type of report")
    add = models.CharField(blank=True, null=True, max_length=600, verbose_name="Can you give more information ?")
    date = models.DateTimeField(default=timezone.now)


class Contentviews(models.Model):
    content = models.ForeignKey(Content, on_delete=models.CASCADE)
    ip = models.GenericIPAddressField()
