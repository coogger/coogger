from core.images.forms import ImageForm
from core.images.models import Image
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ValidationError
from django.shortcuts import redirect, render
from django.views import View

from .configs import DefaultConfig


class Image(LoginRequiredMixin, View):
    model = Image
    form_class = ImageForm
    template_name = "images/index.html"

    def get(self, request):
        context = dict(image_form=self.form_class)
        return render(request, self.template_name, context)

    def post(self, request):
        image_form = self.form_class(request.POST, request.FILES)
        if image_form.is_valid():
            image_form = image_form.save(commit=False)
            if image_form.image.size >= 1048576 * DefaultConfig.max_size:
                raise ValidationError(
                    f"The maximum file size that can be uploaded is {DefaultConfig.max_size}MB"
                )
            image_form.save()
            return redirect(image_form.get_absolute_url)
        return render(request, self.template_name, dict(image_form=image_form))
