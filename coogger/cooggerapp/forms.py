# form
from django.forms import ModelForm

# choices
from cooggerapp.choices import *

# models
from cooggerapp.models import (
    Content, OtherAddressesOfUsers, OtherInformationOfUsers,
    ReportModel)
from django.contrib.auth.models import User


class ContentForm(ModelForm):

    def __init__(self, request=None, *args, **kwargs):
        super(ContentForm, self).__init__(*args, **kwargs)
        if request.dapp_model is not None:
            self.fields["category"].choices = request.categories

    class Meta:
        model = Content
        fields = ["dapp", "category", "language", "topic", "title", "content", "address", "tags"]


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
