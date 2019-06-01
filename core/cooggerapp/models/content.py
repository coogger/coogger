# django
from django.contrib.auth.models import User
from django.db import models
from django.utils.text import slugify
from django.template.loader import render_to_string
from django.conf import settings
from django.db.models import F
from django.urls import reverse
from django.utils import timezone

# models
from .category import Category
from .topic import Topic
from .userextra import OtherInformationOfUsers
from .utils import format_tags
from .utopic import UTopic
from core.django_threadedcomments_system.models import ThreadedComments

# python
from bs4 import BeautifulSoup
from mistune import Markdown, Renderer

# choices
from core.cooggerapp.choices import LANGUAGES, make_choices, STATUS_CHOICES

# 3.part models
from django_md_editor.models import EditorMdField
from django_page_views.models import DjangoViews

# 3.part tags
from django_page_views.templatetags.django_page_views import views_count

# python 
import random

# utils 
from .utils import second_convert

class Content(ThreadedComments):
    body = EditorMdField(
        null=True, 
        blank=True, 
        verbose_name="",
        help_text="Your content | problem | question | or anything else"
    )
    utopic = models.ForeignKey(
        UTopic,
        on_delete=models.CASCADE,
        verbose_name="Your topic",
        help_text="Please, write your topic about your contents.",
    )
    language = models.CharField(
        max_length=30,
        choices=make_choices(LANGUAGES),
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
        choices=make_choices(STATUS_CHOICES),
        verbose_name="content's status",
    )
    mod = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="moderator",
    )  # is it necessary

    class Meta:
        ordering = ["-created"]

    def __str__(self):
        return str(self.get_absolute_url)

    @property
    def get_absolute_url(self):
        return reverse("detail", kwargs=dict(username=str(self.user), permlink=self.permlink))

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
    def utopic_permlink(self):
        return self.utopic.permlink

    @property
    def avatar_url(self):
        return self.user.githubauthuser.avatar_url

    @property
    def views(self):
        return views_count(self.__class__, self.id)

    @property
    def dor(self):
        "duration of read -> second"
        read_char_in_per_second = 28
        body_len = self.body.__len__()
        return body_len / read_char_in_per_second

    @property
    def get_dor(self):
        times = "min"
        for f, t in second_convert(self.dor).items():
            if t != 0:
                times += f" {t} {f} "
        if times == "min":
            return "min 0"
        return times

    def next_or_previous(self, next=True):
        contents = self.__class__.objects.filter(utopic=self.utopic)
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

    def content_save(self, request, form, utopic_permlink):
        self.user = request.user
        user_topic = UTopic.objects.filter(user=self.user, permlink=utopic_permlink)
        self.utopic = user_topic[0]
        self.tags = self.ready_tags()
        self.definition = self.prepare_definition()
        form.save()
        topic_model = Topic.objects.filter(permlink=utopic_permlink)
        topic_model.update(how_many=F("how_many") + 1) # increae how_many in Topic model
        user_topic.update(total_dor=F("total_dor") + self.dor) # increase total dor in utopic
        get_msg = request.POST.get("msg", None)
        if get_msg == "Initial commit":
            get_msg = f"{self.title} Published."
        self.commit_set.model(
            user=self.user,
            utopic=self.utopic,
            content=self,
            body=self.body,
            msg=get_msg,
        ).save()

    def content_update(self, request, old, new):
        # old is a content query
        # new is response a content form
        get_utopic_permlink = request.GET.get("utopic_name", None)
        if get_utopic_permlink is None:
            self.utopic = old[0].utopic
        else:
            self.utopic = UTopic.objects.filter(
                user=old[0].user, 
                permlink=get_utopic_permlink)[0]
        if new.body != old[0].body:
            self.commit_set.model(
                user=old[0].user,
                utopic=self.utopic,
                content=Content.objects.get(user=old[0].user, permlink=old[0].permlink),
                body=new.body,
                msg=request.POST.get("msg")
            ).save()
        old.update(
            utopic=self.utopic,
            definition=self.prepare_definition(),
            category=new.category,
            language=new.language,
            tags=self.ready_tags(),
            body=new.body,
            title=new.title,
            last_update=timezone.now(),
        )

    def ready_tags(self, limit=5):
        return format_tags(self.tags.split(" ")[:limit])
