# django
from django.urls import path

# views
from core.cooggerapp.views.utopic import (
    UserTopic,
    )

urlpatterns = [
    path('<permlink>/@<username>/', UserTopic.as_view(), name="utopic"),
    ]
