from django.forms import ModelForm
from cooggerapp.models import *
from django.contrib.auth.models import User


class ContentForm(ModelForm):
    class Meta:
        model = Blog 
        fields = ["content_list","category","subcategory","category2","title","content","show","tag"]

class AuthorForm(ModelForm):
    class Meta:
        model = Author
        fields = ["sex","county","old","university","jop","iban","phone"]