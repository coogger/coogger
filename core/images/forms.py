from django.forms import ModelForm

from core.images.models import Image


class ImageForm(ModelForm):
    class Meta:
        model = Image
        fields = ["title", "image"]
