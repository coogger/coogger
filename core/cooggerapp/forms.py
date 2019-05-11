# form
from django.forms import ModelForm, CharField

# choices
from core.cooggerapp.choices import *

# models
from core.cooggerapp.models import (
    Content, OtherAddressesOfUsers, OtherInformationOfUsers,
    ReportModel, UTopic, Issue)
from django.contrib.auth.models import User


class UTopicForm(ModelForm):

    class Meta:
        model = UTopic
        fields = ["name", "image_address", "definition", "tags", "address"]


class ContentForm(ModelForm):
    msg = CharField(
        max_length=150, 
        label="Commit Message", 
        help_text="What has changed with this update?"
    )

    class Meta:
        model = Content
        fields = ["category", "language", "title", "body", "tags"]


class OtherAddressesOfUsersForm(ModelForm):
    class Meta:
        model = OtherAddressesOfUsers
        fields = ["choices", "address"]


class CSettingsUserForm(ModelForm):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "username", "email"]


class OtherAddressesOfUsersForm(ModelForm):
    class Meta:
        model = OtherAddressesOfUsers
        fields = ["choices", "address"]


class AboutForm(ModelForm):
    class Meta:
        model = OtherInformationOfUsers
        fields = ["about"]


class CooggerupForm(ModelForm):
    class Meta:
        model = OtherInformationOfUsers
        fields = ["cooggerup_confirmation", "cooggerup_percent"]


class VotepercentForm(ModelForm):
    class Meta:
        model = OtherInformationOfUsers
        fields = ["vote_percent"]


class BeneficiariesForm(ModelForm):
    class Meta:
        model = OtherInformationOfUsers
        fields = ["beneficiaries"]


class ReportsForm(ModelForm):
    class Meta:
        model = ReportModel
        fields = ["complaints", "add"]

class IssueForm(ModelForm):
    class Meta:
        model = Issue
        fields = ["title", "body"]
