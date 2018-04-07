# form
from django.forms import ModelForm

# models
from apps.cooggerapp.models import Content,UserFollow,OtherInformationOfUsers,ReportModel

# user model
from django.contrib.auth.models import User

class ContentForm(ModelForm):
    class Meta:
        model = Content
        fields = ["content_list","title","content","show","tag"]

class UpdateContentForm(ModelForm):
    class Meta:
        model = Content
        fields = ["content_list","content","show","tag"]

class UserFollowForm(ModelForm):
    class Meta:
        model = UserFollow
        fields = ["choices","adress"]

class UserSingupForm(ModelForm):
    class Meta:
        model = User
        fields = ["first_name","last_name","username","email","password"]

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

class ReportsForm(ModelForm):
    class Meta:
        model = ReportModel
        fields = ["complaints","add"]
