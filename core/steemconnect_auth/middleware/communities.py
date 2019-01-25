from django.utils.deprecation import MiddlewareMixin

# models
from core.steemconnect_auth.models import Dapp


class CommunitiesMiddleware(MiddlewareMixin):

    def process_request(self, request):
        model = Dapp
        model_filter = model.objects.filter
        request.dapp_model = model_filter(host_name=request.get_host())[0]
