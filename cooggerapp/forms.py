from django.forms import ModelForm
from cooggerapp.models import Blog,Author,UserFollow
from django.contrib.auth.models import User


class ContentForm(ModelForm):
    class Meta:
        model = Blog 
        fields = ["content_list","category","subcategory","title","content","show","tag"]

class AuthorForm(ModelForm):
    class Meta:
        model = Author
        fields = ["sex","county","old","university","jop","phone"]

class UserFollowForm(ModelForm):
    class Meta:
        model = UserFollow
        fields = ["choices","adress"]