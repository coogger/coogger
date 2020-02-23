from django import forms
from django.contrib.auth.models import User

from apps.cooggerapp.models import (
    Content, Issue, OtherAddressesOfUsers, ReportModel, UTopic
)


class UsernameForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["username"]


class UTopicForm(forms.ModelForm):
    class Meta:
        model = UTopic
        fields = ["name", "image_address", "description", "tags", "address", "status"]


class ContentCreateForm(forms.ModelForm):
    class Meta:
        model = Content
        fields = ["title", "body", "language", "tags", "status"]


class ContentUpdateForm(ContentCreateForm):
    msg = forms.CharField(
        max_length=150,
        label="Commit Message",
        help_text="What has changed with this update?",
    )


class ContentContributeForm(ContentUpdateForm):
    class Meta:
        model = Content
        fields = ["body"]


class AddressesForm(forms.ModelForm):
    class Meta:
        model = OtherAddressesOfUsers
        fields = ["choices", "address"]


class ReportsForm(forms.ModelForm):
    class Meta:
        model = ReportModel
        fields = ["complaints", "add"]


class IssueForm(forms.ModelForm):
    class Meta:
        model = Issue
        fields = ["title", "body"]
