# form
from django import forms

# choices
from core.cooggerapp.choices import *

# models
from core.cooggerapp.models import (
    Content, OtherAddressesOfUsers, OtherInformationOfUsers,
    ReportModel, UTopic, Issue)
    
from django.contrib.auth.models import User


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


class ReplyForm(forms.ModelForm):

    class Meta:
        model = Content
        fields = ["title", "body"]


class OtherAddressesOfUsersForm(forms.ModelForm):
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
        model = OtherInformationOfUsers
        fields = ["about"]


class ReportsForm(forms.ModelForm):
    class Meta:
        model = ReportModel
        fields = ["complaints", "add"]

class NewIssueForm(forms.ModelForm):
    class Meta:
        model = Issue
        fields = ["title", "body"]


class NewIssueReplyForm(forms.ModelForm):
    body = forms.CharField(
        widget=forms.Textarea,
        help_text="problem | question | or anything else")

    class Meta:
        model = Issue
        fields = ["body"]


class NewContentReplyForm(forms.ModelForm):
    body = forms.CharField(
        widget=forms.Textarea,
        help_text="Your content | problem | question | or anything else")
        
    class Meta:
        model = Content
        fields = ["body"]

    


