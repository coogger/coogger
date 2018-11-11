from django.utils.deprecation import MiddlewareMixin
from django.urls import resolve

# models.
from cooggerapp.models import CategoryofDapp, Content
from steemconnect_auth.models import Dapp

# coices
from cooggerapp.choices import *

class GeneralMiddleware(MiddlewareMixin):

    def process_request(self, request):
        if request.dapp_model.name == "coogger":
            category_filter = CategoryofDapp.objects.all()
        else:
            category_filter = CategoryofDapp.objects.filter(dapp=request.dapp_model)
        querysets_list = []
        for category in category_filter:
            querysets = Content.objects.filter(category = category.category_name, status="approved")
            querysets_list.append(querysets)
        categories = []
        for contents in sorted(querysets_list, key=len, reverse=True):
            try:
                categories.append(contents[0].category)
            except IndexError:
                pass
        request.categories = make_choices([category for category in categories])
        request.languages = make_choices(languages)
