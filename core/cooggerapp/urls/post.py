from django.urls import path

# views
from ..views.post import Create, Change

urlpatterns = [
    path('create/<utopic_permlink>/', Create.as_view(), name="create"),
    path('change/@<username>/<permlink>/', Change.as_view(), name="change"),
    ]
