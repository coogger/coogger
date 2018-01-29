#django
from django.http import HttpResponse
from django.contrib import messages as ms
from django.contrib.auth.models import User
from django.db.models import F

# class
from django.views import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

#models
from apps.cooggerapp.models import UserFollow,Content,OtherInformationOfUsers

#views
from apps.cooggerapp.views.tools import is_user_author

#python
import json

class AddressBasedClass(View):
    model = UserFollow

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        if request.is_ajax() and is_user_author(request):
            address_id = int(request.POST["address_id"])
            ubf = self.model.objects.filter(id = address_id)[0]
            if ubf.user == request.user:
                ubf.delete()
            return HttpResponse(json.dumps({"status":"ok","ms":"adres silindi"}))


class ContentBasedClass(View):
    success = "Silme işlemi başarılı"
    error = "hata"

    @method_decorator(login_required)
    def get(self, request,content_id, *args, **kwargs):
        if request.is_ajax() and is_user_author(request):
            queryset = self.really_queryset(request,content_id)
            if request.user == queryset.user:
                queryset.delete()
                OtherInformationOfUsers.objects.filter(user = request.user).update(hmanycontent = F("hmanycontent") -1)
                return HttpResponse(self.success)
            return HttpResponse(self.error)

    @staticmethod
    def really_queryset(request,content_id):
        if request.user.is_superuser:
            queryset = Content.objects.filter(id = content_id)[0]
        else:
            queryset = Content.objects.filter(user = request.user,id = content_id)[0]
        return queryset
