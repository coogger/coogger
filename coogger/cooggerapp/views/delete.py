# django
from django.http import HttpResponse

# class
from django.views import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

# models
from cooggerapp.models import OtherAddressesOfUsers

# python
import json


class Address(View):
    model = OtherAddressesOfUsers

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        if request.is_ajax():
            address_id = int(request.POST["address_id"])
            ubf = self.model.objects.filter(id=address_id)[0]
            if ubf.user == request.user:
                ubf.delete()
            return HttpResponse(json.dumps({"status": "ok", "ms": "Deleted address"}))
