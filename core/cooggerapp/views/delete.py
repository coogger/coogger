# django
from django.http import HttpResponse

# class
from django.views.generic.edit import DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin

# models
from ..models import UserProfile, OtherAddressesOfUsers

# python
import json


class Address(LoginRequiredMixin, DeleteView):

    def post(self, request, *args, **kwargs):
        if request.is_ajax():
            address_id = int(request.POST["address_id"])
            get_address = UserProfile.objects.get(user=request.user)
            get_address.address.remove(OtherAddressesOfUsers.objects.get(id=address_id))
            return HttpResponse(json.dumps({"status": "ok", "ms": "Deleted address"}))
