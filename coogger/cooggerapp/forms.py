# form
from django.forms import ModelForm

# models
from cooggerapp.models import Content,UserFollow,OtherInformationOfUsers,ReportModel

# user model
from django.contrib.auth.models import User

class ContentForm(ModelForm):
    class Meta:
        model = Content
        fields = ["title","content","tag","left_side","right_side"]

class UserFollowForm(ModelForm):
    class Meta:
        model = UserFollow
        fields = ["choices","adress"]

class CSettingsUserForm(ModelForm):
    class Meta:
        model = User
        fields = ["first_name","last_name","username","email"]

class UserFollowForm(ModelForm):
    class Meta:
        model = UserFollow
        fields = ["choices","adress"]

class AboutForm(ModelForm):
    class Meta:
        model = OtherInformationOfUsers
        fields = ["about"]

class CooggerupForm(ModelForm):
    class Meta:
        model = OtherInformationOfUsers
        fields = ["cooggerup_confirmation","cooggerup_percent"]

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
        fields = ["complaints","add"]
