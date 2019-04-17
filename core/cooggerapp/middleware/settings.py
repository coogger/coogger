# django
from django.utils.deprecation import MiddlewareMixin
from django.conf import settings


class SettingsMiddleware(MiddlewareMixin):

    def process_request(self, request):
        request.page_size = settings.PAGE_SIZE