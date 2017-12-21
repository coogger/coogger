from django.forms import ModelForm
from cooggerapp.models import Content,Author,UserFollow
from django.contrib.auth.models import User


class ContentForm(ModelForm):
    class Meta:
        model = Content
        fields = ["title","content","show"]

class AuthorForm(ModelForm):
    class Meta:
        model = Author
        fields = ["sex","county","old","university","jop","phone"]

class UserFollowForm(ModelForm):
    class Meta:
        model = UserFollow
        fields = ["choices","adress"]

class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ["first_name","last_name","username","email"]

class UserFollowForm(ModelForm):
    class Meta:
        model = UserFollow
        fields = ["choices","adress"]
