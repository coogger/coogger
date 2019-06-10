from django.urls import path

# views
from ..views.post import Create, Update

urlpatterns = [
    path('create/<utopic_permlink>/', Create.as_view(), name="create"),
    path('update/@<username>/<permlink>/', Update.as_view(), name="update"),
    ]
