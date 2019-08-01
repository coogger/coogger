import json

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.views.generic.edit import DeleteView

from ..models import OtherAddressesOfUsers, UserProfile


class Address(LoginRequiredMixin, DeleteView):
    def post(self, request, *args, **kwargs):
        address_id = int(request.POST["address_id"])
        get_address = UserProfile.objects.get(user=request.user)
        get_address.address.remove(OtherAddressesOfUsers.objects.get(id=address_id))
        return HttpResponse(json.dumps(dict(status="ok", ms="Deleted address")))
