from django.urls import path

from apps.images.views import Image

from .configs import DefaultConfig

urlpatterns = [
    path(
        DefaultConfig.upload_url,
        Image.as_view(),
        name=DefaultConfig.upload_url_name,
    )
]
