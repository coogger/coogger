from rest_framework.permissions import BasePermission
from django.contrib.auth.models import User
from django.http import Http404

# models
from core.cooggerapp.models import OtherInformationOfUsers
from steemconnect_auth.models import SteemConnectUser

class ApiPermission(BasePermission):
    message = "You don't have permission!"
    my_safe_method = ["GET", "POST"]

    def has_permission(self, request, view):
        if request.user.is_superuser:
            return True
        data = request.data
        try:
            data_access_token = data.get("access_token")
            if data_access_token == "no_permission":
                return None
            get_operation = data.get("operation")
            data_username = data.get("username")
            user = User.objects.filter(username=data_username)[0]
            access_token = OtherInformationOfUsers.objects.filter(user=user)[0].access_token
            user_has_loggedin_before = SteemConnectUser.objects.filter(user=user).exists()
            if not user_has_loggedin_before:
                return False
        except IndexError:
            get_operation = None
        if get_operation == "Filter":
            if user.is_superuser and access_token == data_access_token:
                return True
            return False
        elif get_operation == "Get":
            try:
                if user.is_superuser and access_token == data_access_token:
                    return True
                elif user.username == data_username and access_token == data_access_token:
                    return True
            except KeyError:
                return False
        elif get_operation == "Update":
            try:
                if user.is_superuser and access_token == data_access_token:
                    return True
            except KeyError:
                return False
        elif get_operation == None:
            username = request.GET.get("username", None)
            if username != None:
                if request.user.username == username:
                    return True
            else:
                ApiPermission.message = "use addres if you log in > /?username={your_username}"

    def has_object_permission(self, request, view, obj):
        return self.has_permission(request, view)
