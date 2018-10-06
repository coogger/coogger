from django.utils.deprecation import MiddlewareMixin
from django.urls import resolve

# models.
from cooggerapp.models import CategoryofCommunity

# coices
from cooggerapp.choices import *

class GeneralMiddleware(MiddlewareMixin):

    def process_request(self, request):
        category_objects = CategoryofCommunity.objects
        if request.community_model.name == "coogger":
            category_filter = []
            for category in category_objects.all():
                if category.community.active == True:
                    category_filter.append(category)
        else:
            category_filter = category_objects.filter(community=request.community_model)
        request.categories = make_choices([category.category_name for category in category_filter])
        request.languages = make_choices(languages)
