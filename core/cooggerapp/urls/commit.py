# django
from django.urls import path

# views
from core.cooggerapp.views.commit import (
    Commits,
    CommitDetail,
    )

urlpatterns = [
    path('@<username>/<topic_permlink>/commits/', Commits.as_view(), name="commits"),
    path('@<username>/<topic_permlink>/commit/<hash>/', CommitDetail.as_view(), name="commit"),
    ]
