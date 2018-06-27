from django.conf.urls import url, include
from rest_framework import routers
from api.views import UserViewSet,ContentsViewSet

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'contents', ContentsViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),
]
