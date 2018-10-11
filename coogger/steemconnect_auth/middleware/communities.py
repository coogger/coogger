from django.utils.deprecation import MiddlewareMixin

# models
from steemconnect_auth.models import Community


class CommunitiesMiddleware(MiddlewareMixin):

    def process_request(self, request):
        model = Community
        model_filter = model.objects.filter
        request.community_model = model_filter(host_name=request.get_host())[0]
