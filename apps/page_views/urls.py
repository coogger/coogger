from django.urls import path

from .views import GetView

urlpatterns = [
    path(
        "get-view/<app_label>/<model>/<id>",
        GetView.as_view(),
        name="django-page-views",
    )
]
