from rest_framework.permissions import BasePermission
from cooggerapp.models import OtherInformationOfUsers
from django.contrib.auth.models import User
from django.http import Http404


class ApiPermission(BasePermission):
    message = 'You should write a access_token for allow api services.'
    my_safe_method = ["GET", "POST"]

    def has_permission(self, request, view):
        if request.method in self.my_safe_method:
            try:
                get_operation = request.data["operation"]
                data_username = request.data["username"]
                data_access_token = request.data["access_token"]
                user = User.objects.filter(username=data_username)[0]
                access_token = OtherInformationOfUsers.objects.filter(user=user)[0].access_token
            except:
                get_operation = None
            if get_operation == "Filter":
                if user.is_superuser and access_token == data_access_token:
                    return True
                return False
            elif get_operation == "Update_or_Get":
                try:
                    username = request.parser_context["kwargs"]["username"]
                except KeyError:
                    username = request.parser_context["kwargs"]["pk"].replace("@", "")
                if user.is_superuser and access_token == data_access_token:
                    return True
                elif username == data_username and access_token == data_access_token:
                    return True
                return False
            elif get_operation == None:
                try:
                    username = request.parser_context["kwargs"]["username"]
                except KeyError:
                    return False
                if request.user.is_superuser:
                    return True
                elif request.user.username == username:
                    return True
        return False

    def has_object_permission(self, request, view, obj):
        return self.has_permission(request, view)
