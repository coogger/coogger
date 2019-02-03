# django
from django.utils.text import slugify
from django.contrib.auth.models import User
from django.db import models
from django.utils.timezone import now
from django.template.loader import render_to_string

# choices
from core.cooggerapp.choices import *

# python
from random import randrange

# beem
from beem.comment import Comment
from beem.exceptions import ContentDoesNotExistsException

# steemconnect
from steemconnect.steemconnect import SteemConnect
from steemconnect.operations import (Comment, CommentOptions)

# 3. other
from bs4 import BeautifulSoup
from mistune import Renderer, Markdown

from django_md_editor.models import EditorMdField
from core.steemconnect_auth.models import (SteemConnectUser, Dapp,
    CategoryofDapp, DappSettings)


class Topic(models.Model):
    name = models.CharField(
        unique=True, max_length=50,
        verbose_name="Content topic",
        help_text="Please, write topic name."
        )
    image_address = models.URLField(
        max_length=400,
        blank=True, null=True
        )
    definition = models.CharField(
        max_length=600,
        verbose_name="Definition of topic",
        help_text="Definition of topic",
        blank=True, null=True,
        )
    tags = models.CharField(
        max_length=200,
        blank=True, null=True,
        verbose_name="Keyword",
        help_text="Write your tags using spaces, max:4"
        )
    address = models.URLField(
        blank=True, null=True, max_length=150,
        verbose_name="Add an address if it have"
        )
    editable = models.BooleanField(
        default=True,
        verbose_name="Is it editable? | Yes/No"
        )

    def __str__(self):
        return self.name


class Content(models.Model):
    dapp = models.ForeignKey(Dapp, on_delete=models.CASCADE, help_text="Which application want you share via?")
    user = models.ForeignKey("auth.user", on_delete=models.CASCADE)
    title = models.CharField(max_length=200, verbose_name="Title",
        help_text="Be sure to choose the best title related to your content."
        )
    permlink = models.SlugField(max_length=200)
    content = EditorMdField()
    tags = models.CharField(max_length=200, verbose_name="Keyword",
        help_text="Write your tags using spaces, max:4"
        )
    language = models.CharField(max_length=30, choices=make_choices(languages),
        help_text="The language of your content"
        )
    all_categories = [category.name for category in CategoryofDapp.objects.all()]
    # all_categories = ""
    category = models.CharField(max_length=30,
        choices=make_choices(all_categories),
        help_text="select content category"
        )
    definition = models.CharField(max_length=400,
        verbose_name="Definition of content",
        )
    topic = models.CharField(max_length=50, verbose_name="Content topic",
        help_text="Please, write your topic about your contents."
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
    address = models.URLField(
        blank=True, null=True, max_length=150,
        verbose_name="Add an address about this content if you want"
        )
    created = models.DateTimeField(default=now, verbose_name="Created")
    last_update = models.DateTimeField(default=now, verbose_name="Last update")

    class Meta:
        ordering = ["-created"]

    def __str__(self):
        return f"@{self.user}/{self.permlink}"

    @property
    def get_absolute_url(self):
        return f"/@{self.user.username}/{self.permlink}"

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


    @property
    def username(self):
        return self.user.username

    @property
    def modusername(self):
        return self.mod.username

    @property
    def dapp_name(self):
        return self.dapp.name

    def marktohtml(self, marktext):
        renderer = Renderer(escape=False, parse_block_html=True)
        markdown = Markdown(renderer=renderer)
        return BeautifulSoup(markdown(marktext), "html.parser")

    def get_first_image(self, html_soup):
        img = html_soup.find("img")
        if img is None:
            return ""
        src = img.get("src")
        try:
            alt = img.get("alt")
            if alt == None:
                alt = ""
        except:
            alt = ""
        return f"<img class='definition-img' src='{src}' alt='{alt}'></img>"

    def prepare_definition(self, text):
        soup = self.marktohtml(marktext=text)
        img = self.get_first_image(html_soup=soup)
        if img is None:
            return "<p>{}</p>".format(soup.text[0:200]+"...")
        return f"{img}<p>{soup.text[0:200]}...</p>"

    def definition_for_steem(self, marktext):
        def prepare_text(marktext):
            code_mark = True # closed
            code_mark2 = True # closed
            for_marktext = marktext[0:800].split("\n")
            for line, index in zip(for_marktext, range(len(for_marktext))):
                if line.startswith("```"):
                    code_mark = False # open
                    while True:
                        try:
                            if for_marktext[index+1].startswith("```"):
                                code_mark = True # cloased
                        except IndexError:
                            break
                        index += 1
                elif line.startswith("`"):
                    code_mark2 = False
                    while True:
                        try:
                            if for_marktext[index+1].startswith("`"):
                                code_mark2 = True
                        except IndexError:
                            break
                        index += 1
            if not code_mark:
                return marktext[0:800]+"\n```\n..."
            elif not code_mark2:
                return marktext[0:800]+"\n`\n..."
            return marktext[0:800]+"..."
        soup = self.marktohtml(marktext)
        img = soup.find("img")
        if str(img) not in str(soup)[0:800]:
            image = self.get_first_image(html_soup=soup)
        else:
            image = ""
        return dict(image=image, definition=prepare_text(marktext))

    def save(self, *args, **kwargs):  # for admin.py
        self.topic = slugify(self.topic.lower())
        self.definition = self.prepare_definition(self.content)
        if not Topic.objects.filter(name=self.topic).exists():
            Topic(name=self.topic).save()
        super(Content, self).save(*args, **kwargs)

    def content_save(self, request, *args, **kwargs):
        self.dapp = request.dapp_model
        self.tags = self.ready_tags()
        self.permlink = slugify(self.title.lower())
        self.definition = self.prepare_definition(self.content)
        self.topic = slugify(self.topic.lower())
        while True:
            try: # if user and pemlink is already saved on steem
                Comment(self.get_absolute_url)
                self.new_permlink() #We need to change permlink
            except ContentDoesNotExistsException:
                break
        steem_save = self.steemconnect_post(op_name="save")
        if steem_save.status_code == 200:
            if not Topic.objects.filter(name=self.topic).exists():
                Topic(name=self.topic).save()
            super(Content, self).save(*args, **kwargs)
        return steem_save

    def content_update(self, old, new):
        self.dapp = old[0].dapp
        self.user = old[0].user
        self.permlink = old[0].permlink
        self.title = new.title
        self.address = new.address
        self.definition = self.prepare_definition(new.content)
        self.tags = self.ready_tags(limit=5)
        self.topic = slugify(new.topic.lower())
        steem_post = self.steemconnect_post(op_name="update")
        if steem_post.status_code == 200:
            old.update(
                definition=self.definition,
                topic=self.topic,
                title=self.title,
                address=self.address,
                category=new.category,
                language=new.language,
                tags=self.tags,
            )
        return steem_post

    def steemconnect_post(self, op_name):
        context = dict(
            definition_for_steem=self.definition_for_steem(self.content),
            self=self,
        )
        comment = Comment(
            parent_author = "",
            parent_permlink=self.dapp.name,
            author=str(self.user.username),
            permlink=self.permlink,
            title=self.title,
            body=render_to_string("post/steem-post-note.html", context),
            json_metadata=dict(
                format="markdown",
                tags=self.tags.split(),
                app="coogger/1.4.1",
                ecosystem=dict(
                    name="coogger",
                    version="1.4.1",
                    dapp=self.dapp.name,
                    topic=self.topic,
                    category=self.category,
                    language=self.language,
                    address=self.address,
                    body=self.content,
                )
            ),
        )
        if op_name == "save":
            beneficiaries = self.get_beneficiaries
            if beneficiaries != []:
                comment_options = CommentOptions(parent_comment=comment, beneficiaries=beneficiaries)
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
            sc_dapp_name = steem_connect_user[0].dapp_name
            secret = Dapp.objects.filter(name=sc_dapp_name)[0].app_secret
            access_token = steem_connect_user.set_new_access_token(secret)
            return SteemConnect(token=access_token, data=operation).run

    @property
    def get_beneficiaries(self):
        beneficiaries = []
        if self.dapp.beneficiaries != 0:
            if self.dapp.name != "coogger":
                beneficiaries.append(
                    dict(
                        account=self.dapp.name,
                        weight=self.dapp.beneficiaries * 100
                    )
                )
        user_filter_obj = OtherInformationOfUsers.objects.filter(user=self.user)
        user_beneficiaries = user_filter_obj[0].beneficiaries
        try:
            for_coogger = DappSettings.objects.filter(dapp=self.dapp)[0].beneficiaries
        except IndexError:
            for_coogger = 0
        if user_beneficiaries != 0:
            if for_coogger != 0 and for_coogger > user_beneficiaries:
                beneficiaries.append(
                    dict(
                        account="coogger",
                        weight=for_coogger * 100
                    )
                )
            else:
                beneficiaries.append(
                    dict(
                        account="coogger",
                        weight=user_beneficiaries * 100
                    )
                )
        elif for_coogger != 0:
            beneficiaries.append(
                dict(
                    account="coogger",
                    weight=for_coogger * 100
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
        get_tag.insert(0, self.dapp.name)
        return clearly_tags(get_tag)

    def new_permlink(self):
        self.permlink += "-"+str(randrange(9999))


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
        import hashlib
        sc_user = SteemConnectUser.objects.filter(user=self.user)
        try:
            sc_token = sc_user[0].access_token
        except IndexError:
            return "no_permission"
        return hashlib.sha256(sc_token.encode("utf-8")).hexdigest()


class OtherAddressesOfUsers(models.Model):
    user = models.ForeignKey("auth.user", on_delete=models.CASCADE)
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
    user = models.ForeignKey(
        "auth.user",
        on_delete=models.CASCADE,
        verbose_name="şikayet eden kişi"
    )
    content = models.ForeignKey(
        "content",
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
    content = models.ForeignKey(Content,on_delete=models.CASCADE)
    ip = models.GenericIPAddressField()
