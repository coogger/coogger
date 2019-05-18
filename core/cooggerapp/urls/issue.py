# django
from django.urls import path

# views
from core.cooggerapp.views.issue import (
    IssueView,
    DetailIssue,
    NewIssue,
    ClosedIssue,
    OpenIssue,
    ClosedIssueView,
    )

urlpatterns = [
    path('@<username>/<topic>/issues/', IssueView.as_view(), name="issues"),
    path('@<username>/<topic>/issues/closed', ClosedIssueView.as_view(), name="close-issues"),
    path('@<username>/<topic>/issues/new/', NewIssue.as_view(), name="new-issue"),
    path('@<username>/<topic>/issues/<permlink>/', DetailIssue.as_view(), name="detail-issue"),
    path('@<username>/<topic>/issues/closed/<permlink>/', ClosedIssue.as_view(), name="closed-issue"),
    path('@<username>/<topic>/issues/open/<permlink>/', OpenIssue.as_view(), name="open-issue"),
    ]