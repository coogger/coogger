from rest_framework.permissions import BasePermission
from django.contrib.auth.models import User
from django.http import Http404

# models
from cooggerapp.models import OtherInformationOfUsers
from steemconnect_auth.models import SteemConnectUser

class ApiPermission(BasePermission):
    message = "Something went wrong !"
    my_safe_method = ["GET", "POST"]

    def has_permission(self, request, view):
        if request.user.is_superuser:
            return True
        try:
            get_operation = request.data["operation"]
            data_username = request.data["username"]
            data_access_token = request.data["access_token"]
            user = User.objects.filter(username=data_username)[0]
            access_token = OtherInformationOfUsers.objects.filter(user=user)[0].access_token
            user_has_loggedin_before = SteemConnectUser.objects.filter(user=user).exists()
            if not user_has_loggedin_before:
                return False
        except:
            # to browser
            get_operation = None
        if get_operation == "Filter":
            if user.is_superuser and access_token == data_access_token:
                return True
            return False
        elif get_operation == "Get":
            try:
                username = request.parser_context["kwargs"]["username"]
                if username == data_username and access_token == data_access_token:
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
            try:
                username = request.parser_context["kwargs"]["username"]
                if request.user.username == username:
                    return True
            except KeyError:
                return False

    def has_object_permission(self, request, view, obj):
        return self.has_permission(request, view)
