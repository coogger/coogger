from django.forms import ModelForm
from cooggerapp.models import *

class ContentForm(ModelForm):
    class Meta:
        model = Blog 
        fields = ["content_list","category","subcategory","category2","title","content","tag"]