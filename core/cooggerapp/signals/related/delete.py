from core.bookmark.models import Bookmark
from core.bookmark.utils import get_content_type_with_model
from core.page_views.models import DjangoViews
from core.vote_system.models import Vote, VoteCount


def delete_related_bookmark(model, object_id):
    # Delete related bookmarks obj
    try:
        Bookmark.objects.get(
            content_type=get_content_type_with_model(model), object_id=object_id
        ).delete()
    except Bookmark.DoesNotExist:
        pass


def delete_related_vote(model, object_id):
    try:
        Vote.objects.filter(
            content_type=get_content_type_with_model(model), object_id=object_id
        ).delete()
    except Vote.DoesNotExist:
        pass
    try:
        VoteCount.objects.get(
            content_type=get_content_type_with_model(model), object_id=object_id
        ).delete()
    except VoteCount.DoesNotExist:
        pass


def delete_related_views(model, object_id):
    try:
        DjangoViews.objects.get(
            content_type=get_content_type_with_model(model), object_id=object_id
        ).delete()
    except DjangoViews.DoesNotExist:
        pass
