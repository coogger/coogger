# django
from django.utils.text import slugify
from django.contrib.auth.models import User
from django.db import models
from django.utils.timezone import now
from django.template.loader import render_to_string
from django.conf import settings
from django.db import IntegrityError

# choices
from core.cooggerapp.choices import *

# python
from random import randrange

# steemconnect
from steemconnect.steemconnect import SteemConnect
from steemconnect.operations import (Comment, CommentOptions)

# 3. other
from bs4 import BeautifulSoup
from mistune import Renderer, Markdown

from django_md_editor.models import EditorMdField
from steemconnect_auth.models import SteemConnectUser

# hash
from hashlib import sha256
import uuid

def get_new_hash():
    return sha256(
        str(uuid.uuid4().hex
            ).encode("utf-8")
        ).hexdigest()


class UTopic(models.Model):
    "topic for users"
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.SlugField(
        max_length=50,
        verbose_name="Name",
        help_text="Please, write topic name."
        )
    image_address = models.URLField(
        max_length=400, help_text="Add and Image Address",
        blank=True, null=True
        )
    definition = models.CharField(
        max_length=600,
        help_text="Definition of topic",
        blank=True, null=True,
        )
    tags = models.CharField(
        max_length=200,
        blank=True, null=True,
        verbose_name="Keyword",
        help_text="Write your tags using spaces"
        )
    address = models.URLField(
        blank=True, null=True, max_length=150,
        help_text="Add an address if it have"
        )

    def save(self, *args, **kwargs):
        self.name = slugify(self.name)
        try:
            Topic(name=self.name).save()
        except IntegrityError:
            pass
        super(UTopic, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


class Topic(models.Model):
    "global topic"
    name = models.SlugField(unique=True, max_length=50,
        help_text="Please, write topic name."
        )
    image_address = models.URLField(
        max_length=400,
        blank=True, null=True
        )
    definition = models.CharField(
        max_length=600,
        help_text="Definition of topic",
        blank=True, null=True,
        )
    tags = models.CharField(
        max_length=200,
        blank=True, null=True,
        verbose_name="Keyword",
        help_text="Write your tags using spaces"
        )
    address = models.URLField(
        blank=True, null=True, max_length=150,
        verbose_name="Add an address if it have"
        )
    editable = models.BooleanField(
        default=True,
        verbose_name="Is it editable? | Yes/No"
        )

    def save(self, *args, **kwargs):
        self.name = slugify(self.name)
        super(Topic, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=50)
    template = EditorMdField(blank=True, null=True)

    def save(self, *args, **kwargs):
        self.name = slugify(self.name)
        super(Category, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


class Content(models.Model):
    user = models.ForeignKey("auth.user", on_delete=models.CASCADE)
    permlink = models.SlugField(max_length=200)
    title = models.CharField(max_length=200, verbose_name="Title",
        help_text="Be sure to choose the best title related to your content."
        )
    body = EditorMdField()
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, verbose_name="Your topic",
        help_text="Please, write your topic about your contents."
        )
    language = models.CharField(max_length=30, choices=make_choices(languages),
        help_text="The language of your content"
        )
    category = models.ForeignKey(Category, on_delete=models.CASCADE, help_text="select content category")
    tags = models.CharField(max_length=200, verbose_name="Keywords",
        help_text="Write your tags using spaces, max:4"
        )
    definition = models.CharField(max_length=400,
        verbose_name="Definition of content",
        )
    status = models.CharField(default="approved", max_length=30,
        choices=make_choices(status_choices),
        verbose_name="content's status"
        )
    views = models.IntegerField(default=0, verbose_name="Views")
    mod = models.ForeignKey("auth.user", on_delete=models.CASCADE,
        blank=True, null=True, related_name="moderator"
        )
    cooggerup = models.BooleanField(default=False, verbose_name="Was voting done")
    created = models.DateTimeField(default=now, verbose_name="Created")
    last_update = models.DateTimeField(default=now, verbose_name="Last update")

    class Meta:
        ordering = ["-created"]

    def __str__(self):
        return f"@{self.user}/{self.permlink}"

    @property
    def username(self):
        return self.user.username

    @property
    def modusername(self):
        return self.mod.username

    @property
    def category_name(self):
        return self.category.name

    @property
    def topic_name(self):
        return self.topic.name

    @property
    def utopic(self):
        return UTopic.objects.filter(user=self.user, name=self.topic)[0]

    @property
    def dor(self):
        "duration of read"
        return round(float((self.body.__len__()/28)/60), 3)

    @property
    def get_absolute_url(self):
        return f"/@{self.user.username}/{self.permlink}/"

    @property
    def next_post(self):
        obj = Content.objects.filter(user=self.user, topic=self.topic)
        content_id = obj.filter(permlink=self.permlink)[0].id
        index = 0
        for i, content in zip(range(len(obj)), obj):
            if content.id == content_id:
                index = i
                break
        try:
            return obj[index-1].get_absolute_url
        except (IndexError, AssertionError):
            return False

    @property
    def previous_post(self):
        obj = Content.objects.filter(user=self.user, topic=self.topic)
        content_id = obj.filter(permlink=self.permlink)[0].id
        index = 0
        for i, content in zip(range(len(obj)), obj):
            if content.id == content_id:
                index = i
                break
        try:
            return obj[index+1].get_absolute_url
        except IndexError:
            return False

    @staticmethod
    def marktohtml(marktext):
        renderer = Renderer(escape=False, parse_block_html=True)
        markdown = Markdown(renderer=renderer)
        return BeautifulSoup(markdown(marktext), "html.parser")

    @staticmethod
    def get_first_image(soup):
        img = soup.find("img")
        context = dict(src="", alt="")
        if img is not None:
            context.update(src=img.get("src", ""))
            context.update(alt=img.get("alt", ""))
        return context

    def prepare_definition(self):
        soup = self.marktohtml(self.body)
        first_image = self.get_first_image(soup)
        src, alt = first_image.get("src"), first_image.get("alt")
        if src:
            return f"<img class='definition-img' src='{src}' alt='{alt}'></img><p>{soup.text[:200]}...</p>"
        return f"<p>{soup.text[0:200]}...</p>"

    def save(self, *args, **kwargs):  # for admin.py
        self.definition = self.prepare_definition()
        super(Content, self).save(*args, **kwargs)

    def content_save(self, request, *args, **kwargs):
        self.user = request.user
        self.topic = Topic.objects.filter(name=request.GET.get("topic"))[0]
        self.tags = self.ready_tags()
        self.permlink = slugify(self.title.lower()) # TODO if permlink is not exists on steem share.
        self.definition = self.prepare_definition()
        steem_post = self.steemconnect_post(op_name="save")
        if steem_post.status_code == 200:
            super(Content, self).save(*args, **kwargs)
            utopic = UTopic.objects.filter(user=self.user, name=self.topic)[0]
            get_msg = request.POST.get("msg")
            if get_msg == "Initial commit":
                get_msg = f"{self.title} Published."
            Commit(
                hash = steem_post["result"]["id"],
                user=self.user,
                utopic=utopic,
                content=self,
                body=self.body,
                msg=get_msg
                ).save()
        return steem_post

    def content_update(self, request, old, new):
        self.user = old[0].user
        get_topic_name = request.GET.get("topic", None)
        if get_topic_name is None:
            get_topic_name = old[0].topic
        self.topic = Topic.objects.filter(name=get_topic_name)[0]
        self.body = new.body
        self.permlink = old[0].permlink
        self.title = new.title
        self.category = new.category
        self.language = new.language
        self.tags = self.ready_tags()
        commit_context = dict()
        if self.topic != old[0].topic:
            commit_context["from_topic"] = old[0].topic
            commit_context["to_topic"] = self.topic
        if self.title != old[0].title:
            commit_context["from_title"] = old[0].title
            commit_context["to_title"] = self.title
        if self.category != old[0].category:
            commit_context["from_category"] = old[0].category
            commit_context["to_category"] = self.category
        if self.language != old[0].language:
            commit_context["from_language"] = old[0].language
            commit_context["to_language"] = self.language
        if self.tags != old[0].tags:
            commit_context["from_tags"] = old[0].tags
            commit_context["to_tags"] = self.tags
        if self.body != old[0].body:
            commit_context["body"] = self.body # TODO old[0].body - self.body
        steem_post = self.steemconnect_post(op_name="update")
        if steem_post.status_code == 200:
            old.update(
                body=self.body,
                topic=self.topic,
                definition=self.prepare_definition(),
                title=self.title,
                category=self.category,
                language=self.language,
                tags=self.tags,
            )
            if commit_context != dict():
                Commit(
                    hash = steem_post["result"]["id"],
                    user=self.user,
                    utopic=self.utopic,
                    content=Content.objects.get(user=self.user, permlink=self.permlink),
                    body=render_to_string("post/commit.html", commit_context),
                    msg=request.POST.get("msg"),
                    ).save()
        return steem_post

    def steemconnect_post(self, op_name):
        context = dict(
            image=self.get_first_image(soup=self.marktohtml(self.body)),
            username=self.username,
            permlink=self.permlink,
        )
        comment = Comment(
            parent_author = "",
            parent_permlink="coogger",
            author=str(self.user.username),
            permlink=self.permlink,
            title=self.title,
            body=render_to_string("post/steem-post-note.html", context),
            json_metadata=dict(
                format="markdown",
                tags=self.tags.split(),
                app="coogger/1.4.1",
                ecosystem=dict(
                    version="1.4.1",
                    body=self.body,
                )
            ),
        )
        if op_name == "save":
            if self.get_user_beneficiaries != []:
                comment_options = CommentOptions(parent_comment=comment, beneficiaries=self.get_user_beneficiaries)
                operation = comment_options.operation
            else:
                operation = comment.operation
        elif op_name == "update":
            operation = comment.operation
        steem_connect_user = SteemConnectUser.objects.filter(user=self.user)
        try:
            access_token = steem_connect_user[0].access_token
            return SteemConnect(token=access_token, data=operation).run
        except:
            access_token = steem_connect_user.update_access_token(settings.APP_SECRET)
            return SteemConnect(token=access_token, data=operation).run

    @property
    def get_user_beneficiaries(self):
        beneficiaries = []
        user_benefic = OtherInformationOfUsers.objects.filter(user=self.user)[0].beneficiaries
        if user_benefic != 0:
            beneficiaries.append(
                dict(
                    account="coogger",
                    weight=user_benefic * 100
                )
            )
        return beneficiaries

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
        get_tag = self.tags.split(" ")[:limit]
        get_tag.insert(0, "coogger")
        return clearly_tags(get_tag)


class Commit(models.Model):
    hash = models.CharField(max_length=256, unique=True, default=get_new_hash)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    utopic = models.ForeignKey(UTopic, on_delete=models.CASCADE)
    content = models.ForeignKey(Content, on_delete=models.CASCADE)
    body = EditorMdField()
    msg = models.CharField(max_length=150, default="Initial commit")
    created = models.DateTimeField(default=now, verbose_name="Created")

    class Meta:
        ordering = ["-created"]

    def __str__(self):
        return f"<Commit(content='{self.content}', msg='{self.msg}')>"


class OtherInformationOfUsers(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    about = EditorMdField()
    cooggerup_confirmation = models.BooleanField(default=False,
        verbose_name="Do you want to join in curation trails of the cooggerup bot with your account?"
    )
    sponsor = models.BooleanField(default=False)
    cooggerup_percent = models.FloatField(default=0,
        verbose_name="Cooggerup bot upvote percent"
    )
    vote_percent = models.FloatField(default=100)
    beneficiaries = models.IntegerField(default=0,
        verbose_name="Support Coogger ecosystem with beneficiaries"
    )
    # reward db of coogger.up curation trail, reset per week
    total_votes = models.IntegerField(default=0, verbose_name="How many votes")
    total_vote_value = models.FloatField(default=0, verbose_name="total vote value")
    access_token = models.CharField(max_length=500, default="no_permission")

    @property
    def username(self):
        return self.user.username

    def save(self, *args, **kwargs):
        if self.access_token == "no_permission":
            self.access_token = self.get_new_access_token()
        super(OtherInformationOfUsers, self).save(*args, **kwargs)

    def get_new_access_token(self):
        "creates api_token and user save"
        sc_user = SteemConnectUser.objects.filter(user=self.user)
        if sc_user.exists():
            return get_new_hash()
        return "no_permission"


class OtherAddressesOfUsers(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    choices = models.CharField(
        blank=True,
        null=True, max_length=15,
        choices=make_choices(follow),
        verbose_name="website"
    )
    address = models.CharField(
        blank=True, null=True, max_length=50,
        verbose_name="write address / username"
    )

    @property
    def username(self):
        return self.user.username

    @property
    def get_addresses(self):
        try:
            return OtherAddressesOfUsers.objects.filter(user=self.user)
        except:
            return []

    def __str__(self):
        return self.user.username


class SearchedWords(models.Model):
    word = models.CharField(unique=True, max_length=100)
    hmany = models.IntegerField(default=1)

    def save(self, *args, **kwargs):
        try:
            super(SearchedWords, self).save(*args, **kwargs)
        except:
            SearchedWords.objects.filter(
                word=self.word
            ).update(hmany=models.F("hmany") + 1)


class ReportModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,
        verbose_name="şikayet eden kişi"
    )
    content = models.ForeignKey(Content,
        on_delete=models.CASCADE,
        verbose_name="şikayet edilen içerik"
    )
    complaints = models.CharField(
        choices=make_choices(reports),
        max_length=40, verbose_name="type of report"
    )
    add = models.CharField(
        blank=True, null=True,
        max_length=600,
        verbose_name="Can you give more information ?"
    )
    date = models.DateTimeField(default=now)


class Contentviews(models.Model):
    content = models.ForeignKey(Content, on_delete=models.CASCADE)
    ip = models.GenericIPAddressField()
