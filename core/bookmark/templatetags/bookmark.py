# django
from django import template
from django.core.exceptions import ObjectDoesNotExist

# models
from ..models import Bookmark
# utils
from ..utils import get_content_type_with_model

register = template.Library()


@register.simple_tag
def is_mark(user, model, id):
    if user.is_anonymous:
        return False
    obj = Bookmark.objects.filter(
        content_type=get_content_type_with_model(model), object_id=id
    )
    if obj.filter(user=user).exists():
        return True
    return False


@register.filter
def how_many_mark(model, id):
    try:
        obj = Bookmark.objects.get(
            content_type=get_content_type_with_model(model), object_id=id
        )
    except ObjectDoesNotExist:
        return 0
    return obj.user.count()
