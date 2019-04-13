from django.contrib.auth.models import User
from django.db import models
from django.utils.timezone import now
from django.utils.text import slugify
from django_md_editor.models import EditorMdField

from bs4 import BeautifulSoup
from mistune import Markdown, Renderer

from core.cooggerapp.choices import languages, make_choices, status_choices

from .category import Category
from .topic import Topic
from .userextra import OtherInformationOfUsers
from .utils import format_tags
from .utopic import UTopic


class Content(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    permlink = models.SlugField(max_length=200)
    title = models.CharField(
        max_length=200,
        verbose_name="Title",
        help_text="Be sure to choose the best title related to your content.",
    )
    body = EditorMdField()
    topic = models.ForeignKey(
        Topic,
        on_delete=models.CASCADE,
        verbose_name="Your topic",
        help_text="Please, write your topic about your contents.",
    )
    language = models.CharField(
        max_length=30,
        choices=make_choices(languages),
        help_text="The language of your content",
    )
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, help_text="select content category"
    )
    tags = models.CharField(
        max_length=200,
        verbose_name="Keywords",
        help_text="Write your tags using spaces, max:4",
    )
    definition = models.CharField(max_length=400, verbose_name="Definition of content")
    status = models.CharField(
        default="approved",
        max_length=30,
        choices=make_choices(status_choices),
        verbose_name="content's status",
    )
    views = models.IntegerField(default=0, verbose_name="Views")
    mod = models.ForeignKey(
        "auth.user",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="moderator",
    )  # is it necessary
    cooggerup = models.BooleanField(
        default=False, verbose_name="Was voting done"
    )  # is it necessary
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
        return round(float((self.body.__len__() / 28) / 60), 3)

    @property
    def get_absolute_url(self):
        return f"/@{self.user.username}/{self.permlink}/"

    def next_or_previous(self, next=True):
        contents = self.__class__.objects.filter(user=self.user, topic=self.topic)
        index = list(contents).index(contents.filter(id=self.id)[0])
        if next:
            index = index - 1
        else:
            index = index + 1
        try:
            return contents[index].get_absolute_url
        except (IndexError, AssertionError):
            return False

    @property
    def next_post(self):
        return self.next_or_previous()

    @property
    def previous_post(self):
        return self.next_or_previous(False)

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
        super().save(*args, **kwargs)

    def content_save(self, request, *args, **kwargs):
        self.user = request.user
        self.topic = Topic.objects.filter(name=request.GET.get("topic"))[0]
        self.tags = self.ready_tags()
        self.permlink = slugify(self.title.lower())
        self.definition = self.prepare_definition()
        steem_post = self.steemconnect_post(op_name="save")
        if steem_post.status_code == 200:
            super().save(*args, **kwargs)
            utopic = UTopic.objects.filter(user=self.user, name=self.topic)[0]
            get_msg = request.POST.get("msg")
            if get_msg == "Initial commit":
                get_msg = f"{self.title} Published."
            self.commit_set.model(
                hash=steem_post.json()["result"]["id"],
                user=self.user,
                utopic=utopic,
                content=self,
                body=self.body,
                msg=get_msg,
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
        steem_post = self.steemconnect_post(op_name="update")
        if steem_post.status_code == 200:
            if self.body != old[0].body:
                self.commit_set.model(
                    hash=steem_post.json()["result"]["id"],
                    user=self.user,
                    utopic=self.utopic,
                    content=Content.objects.get(user=self.user, permlink=self.permlink),
                    body=self.body,
                    msg=request.POST.get("msg"),
                ).save()
            old.update(
                body=self.body,
                topic=self.topic,
                definition=self.prepare_definition(),
                title=self.title,
                category=self.category,
                language=self.language,
                tags=self.tags,
                last_update=now(),
            )
        return steem_post

    def steemconnect_post(self, op_name):
        return True
        context = dict(
            image=self.get_first_image(soup=self.marktohtml(self.body)),
            username=self.username,
            permlink=self.permlink,
        )
        comment = Comment(
            parent_author="",
            parent_permlink="coogger",
            author=str(self.user.username),
            permlink=self.permlink,
            title=self.title,
            body=render_to_string("post/steem-post-note.html", context),
            json_metadata=dict(
                format="markdown",
                tags=self.tags.split(),
                app="coogger/1.4.1",
                ecosystem=dict(version="1.4.1", body=self.body),
            ),
        )
        if op_name == "save":
            if self.get_user_beneficiaries != []:
                comment_options = CommentOptions(
                    parent_comment=comment, beneficiaries=self.get_user_beneficiaries
                )
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
        user_benefic = OtherInformationOfUsers.objects.filter(user=self.user)[
            0
        ].beneficiaries
        if user_benefic != 0:
            beneficiaries.append(dict(account="coogger", weight=user_benefic * 100))
        return beneficiaries

    def ready_tags(self, limit=5):
        get_tag = self.tags.split(" ")[:limit]
        get_tag.insert(0, "coogger")
        return format_tags(get_tag)

    @property
    def get_commits(self):  # to api
        context = list()
        fields = ("body", "msg", "created", "body_change")
        queryset = self.commit_set.filter(content=self)
        for c in queryset:
            hash_list = list()
            for h in queryset.filter(hash=c.hash):
                for f in fields:
                    hash_list.append({f: c.__getattribute__(f)})
            context.append({c.hash: hash_list})
        return context

    @property
    def get_report(self):  # to api
        context = list()
        fields = ("complaints", "add", "date")
        queryset = self.reportmodel_set.filter(content=self)
        for c in queryset:
            for f in fields:
                context.append({f: c.__getattribute__(f)})
        return context

    @property
    def get_views(self):  # to api
        context = list()
        fields = ("ip",)
        queryset = self.contentviews_set.filter(content=self)
        for c in queryset:
            for f in fields:
                context.append({f: c.__getattribute__(f)})
        return context


class Contentviews(models.Model):
    content = models.ForeignKey(Content, on_delete=models.CASCADE)
    ip = models.GenericIPAddressField()
