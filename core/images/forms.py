from core.images.models import Image
from django.forms import ModelForm


class ImageForm(ModelForm):
    class Meta:
        model = Image
        fields = ["title", "image"]
