from django import forms

from core.cooggerapp.choices import *
from core.cooggerapp.models import (
    Commit, Content, Issue, OtherAddressesOfUsers, ReportModel, UTopic
)


class UTopicForm(forms.ModelForm):
    class Meta:
        model = UTopic
        fields = ["name", "image_address", "definition", "tags", "address"]


class ContentCreateForm(forms.ModelForm):
    class Meta:
        model = Content
        fields = ["category", "language", "title", "body", "tags", "status"]


class ContentUpdateForm(ContentCreateForm):
    msg = forms.CharField(
        max_length=150,
        label="Commit Message",
        help_text="What has changed with this update?",
    )


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
