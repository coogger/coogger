from django.urls import path

# views
from core.cooggerapp.views.post import Create, Change, CreateUTopic, UpdateUTopic

urlpatterns = [
    path('utopic/<permlink>/', UpdateUTopic.as_view(), name="update-utopic"),
    path('utopic/', CreateUTopic.as_view(), name="create-utopic"),
    path('create/<utopic_permlink>/', Create.as_view(), name="create"),
    path('change/@<username>/<permlink>/', Change.as_view(), name="change"),
    ]
