# django
from django.urls import path

# views
from ..views.settings import Settings


urlpatterns = [
    path('', Settings.as_view(), name="settings"),
    ]