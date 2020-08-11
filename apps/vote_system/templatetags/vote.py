from django import template
from django.contrib.contenttypes.models import ContentType

from ..models import Vote, VoteCount

register = template.Library()


def get_content_type(model):
    content_type_obj = ContentType.objects.get_for_model(model)
    content_type = ContentType.objects.get(
        app_label=content_type_obj.app_label, model=content_type_obj.model
    )
    return content_type


def common_count(model, id):
    return VoteCount.objects.get(
        content_type=get_content_type(model), object_id=id
    )


@register.filter
def upvote_count(model, id):
    return common_count(model, id).upvote_count


@register.filter
def downvote_count(model, id):
    return common_count(model, id).downvote_count


@register.simple_tag
def is_vote(user, model, id):
    if user.is_anonymous:
        return None
    obj = Vote.objects.filter(
        user=user, content_type=get_content_type(model), object_id=id
    )
    if obj.filter(status=True).exists():
        return True
    elif obj.filter(status=False).exists():
        return False
    return None
