from django import forms

from .models import ThreadedComments


class ReplyForm(forms.ModelForm):
    # body = forms.CharField(
    #     widget=forms.Textarea, help_text="problem, question or anything else"
    # )

    class Meta:
        model = ThreadedComments
        fields = ["body"]
