from django.conf.urls import url

#views
from apps.cooggerapp.views import delete

urlpatterns = [
    url(r'^/address/',delete.AddressBasedClass.as_view(),name="address_del"),
    url(r'^/(?P<content_id>.+)/',delete.ContentBasedClass.as_view(),name="content_del"),
    ]
