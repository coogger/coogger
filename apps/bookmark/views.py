from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.views import View

from .models import Bookmark
from .utils import get_content_type


class NewMark(LoginRequiredMixin, View):
    def post(self, request):
        common_parameter = dict(
            content_type=get_content_type(
                app_label=request.POST.get("app_label"),
                model=request.POST.get("model"),
            ),
            object_id=request.POST.get("object_id"),
        )
        book_obj, create = Bookmark.objects.get_or_create(**common_parameter)
        if (
            Bookmark.objects.filter(**common_parameter)
            .filter(user=request.user)
            .exists()
        ):
            book_obj.user.remove(request.user)
            status = False
        else:
            book_obj.user.add(request.user)
            status = True
        return JsonResponse(dict(status=status))
