# form
from django import forms

# choices
from cooggerapp.choices import *

# models
from cooggerapp.models import (
    Content, UserFollow, OtherInformationOfUsers,
    ReportModel, CategoryofCommunity)
from django.db import models
from django.contrib.auth.models import User


class ContentForm(forms.ModelForm):

    def __init__(self, community_model=None, *args, **kwargs):
        super(ContentForm, self).__init__(*args, **kwargs)
        if community_model is not None:
            self.fields["language"].choices = make_choices(languages)
            self.fields["category"].choices = make_choices(self.get_categories(community_model))

    class Meta:
        model = Content
        fields = ["category", "language", "topic", "title", "content", "tag"]

    def get_categories(self, community_model):
        if community_model.name == "coogger":
            category_filter = CategoryofCommunity.objects.all()
        else:
            category_filter = CategoryofCommunity.objects.filter(community=community_model)
        categories = [category.category_name for category in category_filter]
        return categories


class UserFollowForm(forms.ModelForm):
    class Meta:
        model = UserFollow
        fields = ["choices", "adress"]


class CSettingsUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "username", "email"]


class UserFollowForm(forms.ModelForm):
    class Meta:
        model = UserFollow
        fields = ["choices", "adress"]


class AboutForm(forms.ModelForm):
    class Meta:
        model = OtherInformationOfUsers
        fields = ["about"]


class CooggerupForm(forms.ModelForm):
    class Meta:
        model = OtherInformationOfUsers
        fields = ["cooggerup_confirmation", "cooggerup_percent"]


class VotepercentForm(forms.ModelForm):
    class Meta:
        model = OtherInformationOfUsers
        fields = ["vote_percent"]


class BeneficiariesForm(forms.ModelForm):
    class Meta:
        model = OtherInformationOfUsers
        fields = ["beneficiaries"]


class ReportsForm(forms.ModelForm):
    class Meta:
        model = ReportModel
        fields = ["complaints", "add"]
