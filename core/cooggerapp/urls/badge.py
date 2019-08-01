from django.urls import path

from ..views.badge import BadgeView

urlpatterns = [path("badge/<permlink>/", BadgeView.as_view(), name="badge")]
