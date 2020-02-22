from django import forms

from .models import ThreadedComments


class ReplyForm(forms.ModelForm):
    class Meta:
        model = ThreadedComments
        fields = ["body"]
