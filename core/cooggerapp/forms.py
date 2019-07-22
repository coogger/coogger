# django
from django import forms
from django.contrib.auth.models import User

# choices
from core.cooggerapp.choices import *

# models
from core.cooggerapp.models import (
    Content, OtherAddressesOfUsers, UserProfile,
    ReportModel, UTopic, Issue)

from .models.utils import send_mail


class UTopicForm(forms.ModelForm):

    class Meta:
        model = UTopic
        fields = ["name", "image_address", "definition", "tags", "address"]


class ContentForm(forms.ModelForm):
    msg = forms.CharField(
        max_length=150, 
        label="Commit Message", 
        help_text="What has changed with this update?"
    )

    class Meta:
        model = Content
        fields = ["category", "language", "title", "body", "tags"]
    
    @classmethod
    def send_mail(cls, form):
        send_mail(
            subject = f"{form.user} publish a new content | coogger".title(),
            template_name="email/post.html", 
            context=dict(
                get_absolute_url=form.get_absolute_url
            ),
            to=[u.user.email for u in form.user.follow.follower if u.user.email], 
        )


class AddressesForm(forms.ModelForm):
    class Meta:
        model = OtherAddressesOfUsers
        fields = ["choices", "address"]


class CSettingsUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "username", "email"]


class OtherAddressesOfUsersForm(forms.ModelForm):
    class Meta:
        model = OtherAddressesOfUsers
        fields = ["choices", "address"]


class AboutForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ["about"]


class ReportsForm(forms.ModelForm):
    class Meta:
        model = ReportModel
        fields = ["complaints", "add"]

class IssueForm(forms.ModelForm):
    class Meta:
        model = Issue
        fields = ["title", "body"]

    @classmethod
    def send_mail(cls, form):
        send_mail(
            subject=f"{form.user} opened a new issue on your {form.utopic.name} topic | coogger".title(), 
            template_name="email/new-issue.html", 
            context=dict(
                form=form,
            ),
            to=[form.utopic.user.email]
        )


class IssueReplyForm(forms.ModelForm):
    body = forms.CharField(
        widget=forms.Textarea,
        help_text="problem | question | or anything else")

    class Meta:
        model = Issue
        fields = ["body"]


class ContentReplyForm(IssueReplyForm):

    class Meta(IssueReplyForm.Meta):
        model = Content