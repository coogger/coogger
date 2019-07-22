# django
from django.urls import path

# views
from ..views.issue import (
    IssueView,
    DetailIssue,
    NewIssue,
    ClosedIssue,
    OpenIssue,
    ClosedIssueView,
    UpdateIssue
    )

urlpatterns = [
    path(
        '@<username>/<utopic_permlink>/issues/', 
        IssueView.as_view(), 
        name="issues"
    ),
    path(
        '@<username>/<utopic_permlink>/issues/closed', 
        ClosedIssueView.as_view(), 
        name="close-issues"
    ),
    path(
        '@<username>/<utopic_permlink>/issues/new/', 
        NewIssue.as_view(), 
        name="new-issue"
    ),
    path(
        '@<username>/<utopic_permlink>/issues/<permlink>/update/', 
        UpdateIssue.as_view(), 
        name="update-issue"
    ),
    path(
        '@<username>/<utopic_permlink>/issues/<permlink>/', 
        DetailIssue.as_view(), 
        name="detail-issue"
    ),
    path(
        '@<username>/<utopic_permlink>/issues/closed/<permlink>/', 
        ClosedIssue.as_view(), 
        name="closed-issue"
    ),
    path(
        '@<username>/<utopic_permlink>/issues/open/<permlink>/', 
        OpenIssue.as_view(), 
        name="open-issue"
    ),
    ]