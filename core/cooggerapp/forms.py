# form
from django.forms import ModelForm

# choices
from core.cooggerapp.choices import *

# models
from core.cooggerapp.models import (
    Content, OtherAddressesOfUsers, OtherInformationOfUsers,
    ReportModel, UTopic)
from django.contrib.auth.models import User


class UTopicForm(ModelForm):

    class Meta:
        model = UTopic
        fields = ["name", "image_address", "definition", "tags", "address"]


class ContentForm(ModelForm):

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
