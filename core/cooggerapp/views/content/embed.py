from django.utils.decorators import method_decorator
from django.views.decorators.clickjacking import xframe_options_exempt

from .detail import Detail


@method_decorator(xframe_options_exempt, name="dispatch")
class Embed(Detail):
    template_name = "content/detail/embed.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["embed"] = True
        return context
