from django.utils.deprecation import MiddlewareMixin
from django.urls import resolve

# models.
# from cooggerapp.models import Community

# coices
from cooggerapp.choices import *

class GeneralMiddleware(MiddlewareMixin):

    def process_request(self, request):
        request.categories = make_choices(eval(request.community_model.name+"_categories"))
        request.languages = make_choices(languages)
