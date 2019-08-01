from django.urls import path

from ..views.utopic import CreateUTopic, DetailUserTopic, UpdateUTopic

urlpatterns = [
    path("<permlink>/@<username>/", DetailUserTopic.as_view(), name="detail-utopic"),
    path("utopic/<permlink>/", UpdateUTopic.as_view(), name="update-utopic"),
    path("utopic/", CreateUTopic.as_view(), name="create-utopic"),
]
