#django
from django.http import HttpResponseRedirect
from django.contrib import messages as ms
from django.contrib.auth import logout

# class
#from django.views.generic import ListView
from django.views import View

#models
from apps.cooggerapp.models import OtherInformationOfUsers


class Logout(View):
    error = "Çıkış yapılırken beklenmedik hata oluştur"
    success = "Tekrar görüşmek üzere {}"

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            ms.success(request,self.success.format(request.user))
            logout(request)
        return HttpResponseRedirect("/")
