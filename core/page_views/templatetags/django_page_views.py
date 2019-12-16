from django import template
from django.contrib.contenttypes.models import ContentType

from ..models import DjangoViews

register = template.Library()


@register.filter(name="views_count")
def views_count(model, id):
    content_type_obj = ContentType.objects.get_for_model(model)
    content_type = ContentType.objects.get(
        app_label=content_type_obj.app_label, model=content_type_obj.model
    )
    model = DjangoViews
    query = model.objects.filter(content_type=content_type, object_id=id)
    try:
        return query[0].views_count
    except IndexError:
        return 0
