# django
from django.urls import path

# views
from core.cooggerapp.views.utopic import (
    UserTopic, CreateUTopic, UpdateUTopic
    )

urlpatterns = [
    path('<permlink>/@<username>/', UserTopic.as_view(), name="utopic"),
    path('utopic/<permlink>/', UpdateUTopic.as_view(), name="update-utopic"),
    path('utopic/', CreateUTopic.as_view(), name="create-utopic"),
]
