from django.utils.deprecation import MiddlewareMixin
from django.urls import resolve

# models.
from cooggerapp.models import CategoryofCommunity

# coices
from cooggerapp.choices import *

class GeneralMiddleware(MiddlewareMixin):

    def process_request(self, request):
        if request.community_model.name == "coogger":
            category_filter = CategoryofCommunity.objects.all()
        else:
            category_filter = CategoryofCommunity.objects.filter(community=request.community_model)
        request.categories = make_choices([category.category_name for category in category_filter])
        request.languages = make_choices(languages)
