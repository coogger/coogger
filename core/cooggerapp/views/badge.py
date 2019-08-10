from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView
from djangobadge.models import Badges


class BadgeView(TemplateView):
    template_name = "badge/detail.html"

    def get_context_data(self, permlink, *args, **kwargs):
        queryset = get_object_or_404(Badges, permlink=permlink)
        context = super().get_context_data(**kwargs)
        context["queryset"] = queryset
        return context
