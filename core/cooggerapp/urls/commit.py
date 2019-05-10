# django
from django.urls import path

# views
from core.cooggerapp.views.commit import (
    Commits,
    CommitDetail,
    )

urlpatterns = [
    path('@<username>/<topic>/commits/', Commits.as_view(), name="commits"),
    path('@<username>/<topic>/commit/<hash>/', CommitDetail.as_view(), name="commit"),
    ]
