from django.urls import path

from .views import NewMark

app_name = "bookmark"
urlpatterns = [path("add_or_remove/", NewMark.as_view(), name="add_or_remove")]
