# django
from django.contrib.auth.models import User
from django.db import models
from django.db.models import F
from django.urls import reverse
from django.utils import timezone

# models
from .category import Category
from .topic import Topic
from .utils import format_tags
from .topic import UTopic
from .threaded_comments import ThreadedComments

# choices
from core.cooggerapp.choices import LANGUAGES, make_choices, STATUS_CHOICES

# 3.part models
from django_md_editor.models import EditorMdField

# 3.part tags
from django_page_views.templatetags.django_page_views import views_count
from django_vote_system.templatetags.vote import upvote_count, downvote_count

# python 
import random

# utils 
from .utils import (
    second_convert, marktohtml, 
    get_first_image, dor, NextOrPrevious,
    send_mail
    )

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
        unique_together = [["user", "permlink"]]

    def __str__(self):
        return str(self.get_absolute_url)

    @property
    def get_absolute_url(self):
        return reverse("detail", kwargs=dict(username=str(self.user), permlink=self.permlink))

    @property
    def views(self):
        return views_count(self.__class__, self.id)

    @property
    def upvote_count(self):
        return upvote_count(self.__class__, self.id)

    @property
    def downvote_count(self):
        return downvote_count(self.__class__, self.id)

    @property
    def get_dor(self):
        times = "min"
        for f, t in second_convert(dor(self.body)).items():
            if t != 0:
                times += f" {t} {f} "
        if times == "min":
            return "min 0"
        return times

    def next_or_previous(self, next=True):
        filter_field = dict(
            user=self.user, utopic=self.utopic, reply=None
        )
        n_or_p = NextOrPrevious(self.__class__, filter_field, self.id)
        if next:
            return n_or_p.next_query
        return n_or_p.previous_query

    @property
    def next_post(self):
        try:
            return self.next_or_previous().get_absolute_url
        except AttributeError:
            return False

    @property
    def previous_post(self):
        try:
            return self.next_or_previous(next=False).get_absolute_url
        except AttributeError:
            return False

    def prepare_definition(self):
        soup = marktohtml(self.body)
        first_image = get_first_image(soup)
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
        form.save() # content save
        user_topic.update(how_many=F("how_many") + 1)
        topic_model = Topic.objects.filter(permlink=utopic_permlink)
        topic_model.update(how_many=F("how_many") + 1) # increae how_many in Topic model
        user_topic.update(total_dor=F("total_dor") + dor(self.body)) # increase total dor in utopic
        get_msg = request.POST.get("msg", None)
        if get_msg == "Initial commit":
            get_msg = f"{self.title} Published."
        self.commit_set.model(
            user=self.user,
            utopic=self.utopic,
            content=self,
            body=self.body,
            msg=get_msg,
        ).save() # commit save
        # send mail
        subject = f"{self.user} publish a new content | coogger".title()
        context = dict(
            get_absolute_url=self.get_absolute_url
        )
        send_mail(
            subject=subject, user=self.user, 
            template_name="email/post.html", 
            context=context
        )

    def content_update(self, request, old, new):
        # old is a content query
        # new is response a content form
        if old[0].reply is not None:
            "if its a comment"
            self.body = new.body
            old.update(
                title=new.title,
                body=self.body,
                definition=self.prepare_definition(),
                last_update=timezone.now(),
            )
        else:
            get_utopic_permlink = request.GET.get("utopic_permlink", None)
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
                    content=old[0],
                    body=new.body,
                    msg=request.POST.get("msg")
                ).save()
            self.body = new.body
            old.update(
                definition=self.prepare_definition(),
                category=new.category,
                language=new.language,
                tags=self.ready_tags(),
                body=self.body,
                title=new.title,
                last_update=timezone.now(),
                utopic=self.utopic,
            )

    def ready_tags(self, limit=5):
        return format_tags(self.tags.split(" ")[:limit])
