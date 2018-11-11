from django.utils.deprecation import MiddlewareMixin
from django.urls import resolve

# models.
from cooggerapp.models import CategoryofDapp
from steemconnect_auth.models import Dapp

# coices
from cooggerapp.choices import *

class GeneralMiddleware(MiddlewareMixin):

    def process_request(self, request):
        category_objects = CategoryofDapp.objects
        if request.dapp_model.name == "coogger":
            category_filter = []
            for category in category_objects.all():
                if category.dapp.active == True:
                    category_filter.append(category)
        else:
            category_filter = category_objects.filter(dapp=request.dapp_model)
        request.categories = make_choices([category.category_name for category in category_filter])
        request.languages = make_choices(languages)
        dapp_filter = Dapp.objects.filter(active=True)
        request.dapps = make_choices([dapp.name for dapp in dapp_filter])
