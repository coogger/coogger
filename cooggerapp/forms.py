from django.forms import ModelForm
from cooggerapp.models import *

# Create the form class.

class CommentForm(ModelForm):
     class Meta:
         model = Comment
         fields = ["comment"]

class ContentForm(ModelForm):
    class Meta:
        model = Blog 
        fields = ["content_list","category","subcategory","category2","title","content","tag"]
