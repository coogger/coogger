# django
from django.utils.deprecation import MiddlewareMixin

# models
from ..models import IpModel


class IpMiddleware(MiddlewareMixin):
    def process_request(self, request):
        ip_address = self.get_ip_address(request)
        if ip_address is None:
            request.ip_model = None
        else:
            query = IpModel.objects.filter(ip=ip_address)
            if not query.exists() and ip_address is not None:
                IpModel(ip=ip_address).save()
                request.ip_model = IpModel.objects.get(ip=ip_address)
            else:
                request.ip_model = query[0]

    @staticmethod
    def get_ip_address(request):
        try:
            return str(
                request.META["HTTP_X_FORWARDED_FOR"].split(",")[-1].strip()
            )
        except:
            return str(request.META["REMOTE_ADDR"])
