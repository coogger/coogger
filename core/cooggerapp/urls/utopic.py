# django
from django.urls import path

# views
from core.cooggerapp.views.utopic import (
    UserTopic,
    Commits,
    CommitDetail,
    Issue
    )

urlpatterns = [
    path('<topic>/@<username>/', UserTopic.as_view(), name="utopic"),
    path('@<username>/<topic>/commits/', Commits.as_view(), name="commits"),
    path('@<username>/<topic>/issues/', Issue.as_view(), name="issues"),
    path('@<username>/<topic>/commit/<hash>/', CommitDetail.as_view(), name="commit"),
    ]
