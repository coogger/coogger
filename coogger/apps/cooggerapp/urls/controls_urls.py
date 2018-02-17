from django.conf.urls import url

#views
from apps.cooggerapp.views import controls

urlpatterns = [
    url(r'^/create/',controls.Create.as_view(),name="cooggerapp-create"),
    url(r'^/change/(?P<content_id>.+)/',controls.Change.as_view(),name="cooggerapp-change"),
    ]
