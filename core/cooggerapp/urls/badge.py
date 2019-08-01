# django
from django.urls import path

# views
from ..views.badge import BadgeView

urlpatterns = [path("badge/<permlink>/", BadgeView.as_view(), name="badge")]
