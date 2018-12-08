# django
from django.utils.text import slugify
from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone

# choices
from cooggerapp.choices import *

# python
import random

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
from steemconnect_auth.models import (SteemConnectUser, Dapp,
    CategoryofDapp, DappSettings)


class Content(models.Model):
    dapp = models.ForeignKey(Dapp, on_delete=models.CASCADE, help_text="Which application want you share via?")
    user = models.ForeignKey("auth.user", on_delete=models.CASCADE)
    title = models.CharField(max_length=200, verbose_name="Title",
        help_text="Be sure to choose the best title related to your content."
    )
    permlink = models.SlugField(max_length=200)
    content = EditorMdField() # not necessary
    tag = models.CharField(max_length=200, verbose_name="keyword",
        help_text="Write your tags using spaces, max:4"
    )
    language = models.CharField(max_length=30, choices=make_choices(languages),
        help_text=" The language of your content"
    )
    all_categories = [category.category_name for category in CategoryofDapp.objects.all()]
    # all_categories = ""
    category = models.CharField(max_length=30,
        choices=make_choices(all_categories),
        help_text="select content category"
    )
    definition = models.CharField(max_length=400,
        verbose_name="definition of content",
    )
    topic = models.CharField(max_length=50, verbose_name="content topic",
        help_text="Please, write your topic about your contents."
    )
    status = models.CharField(default="shared", max_length=30,
        choices=make_choices(status_choices),
        verbose_name="content's status"
    )
    views = models.IntegerField(default=0, verbose_name="views")
    mod = models.ForeignKey("auth.user", on_delete=models.CASCADE,
        blank=True, null=True, related_name="moderator"
    )
    cooggerup = models.BooleanField(default=False, verbose_name="was voting done")

    class Meta:
        ordering = ["-id"]

    @property
    def username(self):
        return self.user.username

    @property
    def modusername(self):
        return self.mod.username

    @property
    def dapp_name(self):
        return self.dapp.name

    def __str__(self):
        return f"@{self.user}/{self.permlink}"

    def marktohtml(self, marktext):
        renderer = mistune.Renderer(escape=False, parse_block_html=True)
        markdown = mistune.Markdown(renderer=renderer)
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
            code_mark = True
            code_mark2 = True
            for_marktext = marktext[0:800].split("\n")
            for line, index in zip(for_marktext, range(len(for_marktext))):
                if line.startswith("```") or "```" in line:
                    code_mark = False
                    while True:
                        try:
                            if for_marktext[index] == "```":
                                code_mark = True
                        except IndexError:
                            break
                        index += 1
                elif line.startswith("`") or "```" in line:
                    code_mark2 = False
                    while True:
                        try:
                            if for_marktext[index] == "`":
                                code_mark2 = True
                        except IndexError:
                            break
                        index += 1
            if not code_mark:
                return marktext[0:800]+"\n```\n"
            elif not code_mark2:
                return marktext[0:800]+"\n`\n"
            else:
                return marktext[0:800]
        soup = self.marktohtml(marktext)
        img = soup.find("img")
        if str(img) not in str(soup)[0:800]:
            img = f"<center>{self.get_first_image(html_soup=soup)}</center>\n\n"
        else:
            img = ""
        definiton_mark = f"{prepare_text(marktext)}...\n\n<hr>\n\nRead this content\
         on [www.coogger.com](www.coogger.com/@{self.user.username}/{self.permlink})\n"
        return img+definiton_mark

    @property
    def get_absolute_url(self):
        return "@"+self.user.username+"/"+self.permlink

    def save(self, *args, **kwargs):  # for admin.py
        self.topic = slugify(self.topic.lower())
        # if self.mod == User.objects.get(username="hakancelik"):
        #     try:
        #         POST = Post(post=f"@{self.user}/{self.permlink}")
        #         self.steemconnect_post(self.permlink, "update")
        #     except:
        #         steem_post = self.steemconnect_post(self.permlink, "save")
        self.definition = self.prepare_definition(self.content)
        super(Content, self).save(*args, **kwargs)

    def save_for_sync(self, *args, **kwargs):
        "To sync coogger.db"
        try:
            POST = Post(post=f"@{self.user}/{self.permlink}")
            self.content = POST.body
            self.definition = self.prepare_definition(self.content)
            super(Content, self).save(*args, **kwargs)
        except:
            pass

    def content_save(self, request, *args, **kwargs):
        self.dapp = request.dapp_model
        self.tag = self.ready_tags()
        self.permlink = slugify(self.title.lower())
        self.definition = self.prepare_definition(self.content)
        self.topic = slugify(self.topic.lower())
        while True:
            try: # if user and pemlink is already saved on steem
                Post(post=self.get_absolute_url).url
                self.new_permlink() #We need to change permlink
            except:
                break
        steem_save = self.steemconnect_post(self.permlink, "save")
        if steem_save.status_code == 200:
            super(Content, self).save(*args, **kwargs)
        return steem_save

    def content_update(self, queryset, content):
        self.dapp = queryset[0].dapp
        self.user = queryset[0].user
        self.title = content.title
        self.permlink = queryset[0].permlink
        self.definition = self.prepare_definition(content.content)
        self.tag = self.ready_tags(limit=5)
        self.topic = slugify(content.topic.lower())
        steem_post = self.steemconnect_post(self.permlink, "update")
        if steem_post.status_code == 200:
            queryset.update(
                definition=self.definition,
                topic=self.topic,
                title=self.title,
                category=content.category,
                language=content.language,
                tag=self.tag,
            )
        return steem_post

    def steemconnect_post(self, permlink, json_metadata):
        def_name = json_metadata
        if json_metadata == "save":
            self.content += "\n"+self.dapp.ms.format(self.get_absolute_url)
        json_metadata = {
            "format": "markdown",
            "tags": self.tag.split(),
            "app": "coogger/1.4.1",
            "ecosystem": {
                "name": "coogger",
                "version": "1.4.1",
                "dapp": self.dapp.name,
                "topic": self.topic,
                "category": self.category,
                "language": self.language,
                "body": self.content,
                },
        }
        body_for_steem = f"""{self.definition_for_steem(self.content)}\n
- Dapp; [Coogger]({self.dapp.host_name})
- Category; [Tutorial](https://www.coogger.com/category/{self.category}/)
- Language; [Turkish](https://www.coogger.com/language/{self.language}/)
- Topic; [Python](https://www.coogger.com/python/@{self.user.username}/)
- Filter;[username={self.user.username}&category={self.category}&topic={self.topic}&language={self.language}](https://www.coogger.com/filter/?username={self.user.username}&category={self.category}&topic={self.topic}&language={self.language})
- User; [@{self.user.username}](www.coogger.com/@{self.user.username})<br>

--------

Posted using [www.coogger.com](https://www.coogger.com)
Coogger is an ecosystem where is **knowledge sharing network** which can **build web dapps** and **groups**

#### Contact Us

- [on Spectrum](https://spectrum.chat/coogger)
- [on Discord](https://discord.gg/avmdZJa)"""
        comment = Comment(
            parent_author = "",
            parent_permlink=self.dapp.name,
            author=str(self.user.username),
            permlink=permlink,
            title=self.title,
            body=body_for_steem,
            json_metadata=json_metadata,
        )
        if def_name == "save":
            beneficiaries = self.get_beneficiaries()
            if beneficiaries != []:
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
            sc_dapp_name = steem_connect_user[0].dapp_name
            secret = Dapp.objects.filter(name=sc_dapp_name)[0].app_secret
            access_token = steem_connect_user.set_new_access_token(secret)
            return SteemConnect(token=access_token, data=operation).run

    def get_beneficiaries(self):
        beneficiaries = []
        dapp_beneficiaries = self.dapp.beneficiaries
        other_user_beneficiaries = OtherInformationOfUsers.objects.filter(user=self.user)[0].beneficiaries
        dapp_beneficiaries_for_coogger = DappSettings.objects.filter(dapp=self.dapp)[0].beneficiaries
        if dapp_beneficiaries != 0:
            if self.dapp.name != "coogger":
                beneficiaries.append({"account": self.dapp.name, "weight": dapp_beneficiaries*100})
        if other_user_beneficiaries != 0:
            if dapp_beneficiaries_for_coogger != 0 and dapp_beneficiaries_for_coogger>other_user_beneficiaries:
                beneficiaries.append({"account": "coogger", "weight": dapp_beneficiaries_for_coogger*100})
            else:
                beneficiaries.append({"account": "coogger", "weight": other_user_beneficiaries*100})
        elif dapp_beneficiaries_for_coogger != 0:
            beneficiaries.append({"account": "coogger", "weight": dapp_beneficiaries_for_coogger*100})
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
        get_tag = self.tag.split(" ")[:limit]
        get_tag.insert(0, self.dapp.name)
        return clearly_tags(get_tag)

    def new_permlink(self):
        rand = str(random.randrange(9999))
        self.permlink += "-"+rand


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

    def save_with_access_token(self, *args, **kwargs):
        "creates api_token"
        import hashlib
        hash_object = hashlib.sha256(self.access_token.encode('utf-8'))
        hex_dig = hash_object.hexdigest()
        self.access_token = hex_dig
        super(OtherInformationOfUsers, self).save(*args, **kwargs)


class OtherAddressesOfUsers(models.Model):
    user = models.ForeignKey("auth.user", on_delete=models.CASCADE)
    choices = models.CharField(blank=True, null=True, max_length=15, choices=make_choices(follow), verbose_name="website")
    address = models.CharField(blank=True, null=True, max_length=150, verbose_name="write address / username")

    @property
    def username(self):
        return self.user.username

    def __str__(self):
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
