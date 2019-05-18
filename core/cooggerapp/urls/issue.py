# django
from django.urls import path

# views
from core.cooggerapp.views.issue import (
    IssueView,
    DetailIssue,
    NewIssue
    )

urlpatterns = [
    path('@<username>/<topic>/issues/', IssueView.as_view(), name="issues"),
    path('@<username>/<topic>/issues/new/', NewIssue.as_view(), name="new-issue"),
    path('@<username>/<topic>/issues/<permlink>/', DetailIssue.as_view(), name="detail-issue"),
    ]