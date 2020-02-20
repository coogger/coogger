from django.contrib.contenttypes.models import ContentType
from django.db import IntegrityError
from django.shortcuts import render

from core.page_views.models import DjangoViews


class CommonDetailView(object):
    """
    This class provides detail object and make a reply,
    subclass must write a function named get_object
    """

    model = None
    model_name = None
    template_name = None
    form_class = None

    def save_view(self, request, id):  # TODO use reqeust/response signals
        get_view, created = DjangoViews.objects.get_or_create(
            content_type=ContentType.objects.get(
                app_label="cooggerapp", model=self.model_name
            ),
            object_id=id,
        )
        try:
            get_view.ips.add(request.ip_model)
        except IntegrityError:
            pass

    def get_context_data(self, **kwargs):
        return dict(queryset=self.get_object(**kwargs), form=self.form_class)

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        queryset = context.get("queryset")
        self.save_view(request, queryset.id)
        return render(request, self.template_name, context)
