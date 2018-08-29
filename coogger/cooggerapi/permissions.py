from rest_framework.permissions import BasePermission

class ApiPermission(BasePermission):
    message = 'You should take a key for allow api services.'
    my_safe_method = ["GET", "POST"]

    def has_permission(self, request, view):
        api_key = request.data.get("api_key")
        if request.method in self.my_safe_method and api_key == "api_key":
            # TODO: developing these codes
            return True
        return False

    def has_object_permission(self, request, view, obj):
        api_key = request.data.get("api_key")
        if request.method in self.my_safe_method and api_key == "api_key":
            return True
        return False
