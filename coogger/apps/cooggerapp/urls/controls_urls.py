from django.conf.urls import url

#views
from apps.cooggerapp.views import controls

urlpatterns = [
    url(r'^/create/',controls.CreateBasedClass.as_view(),name="create"),
    url(r'^/change/(?P<content_id>.+)/',controls.ChangeBasedClass.as_view(),name="change"),
    ]
