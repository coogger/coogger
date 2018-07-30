from django.utils.deprecation import MiddlewareMixin

#models
from django_steemconnect.models import Community

class CommunitiesMiddleware(MiddlewareMixin):

    def process_request(self, request):
        request.community_model = Community.objects.filter(host_name = request.get_host())[0]
