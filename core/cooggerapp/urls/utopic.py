# django
from django.urls import path

# views
from ..views.utopic import DetailUserTopic, CreateUTopic, UpdateUTopic

urlpatterns = [
    path("<permlink>/@<username>/", DetailUserTopic.as_view(), name="detail-utopic"),
    path("utopic/<permlink>/", UpdateUTopic.as_view(), name="update-utopic"),
    path("utopic/", CreateUTopic.as_view(), name="create-utopic"),
]
