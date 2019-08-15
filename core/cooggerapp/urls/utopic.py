from django.urls import path

from ..views.utopic import (
    ClosedIssue,
    ClosedIssueView,
    CommitDetail,
    Commits,
    CommitUpdate,
    Contribution,
    Contributor,
    CreateUTopic,
    DetailIssue,
    DetailUserTopic,
    IssueView,
    NewIssue,
    OpenIssue,
    UpdateIssue,
    UpdateUTopic,
)

urlpatterns = [
    path("@<username>/<topic_permlink>/commits/", Commits.as_view(), name="commits"),
    path(
        "@<username>/<topic_permlink>/commit/<hash>/",
        CommitDetail.as_view(),
        name="commit",
    ),
    path("commit/update/<hash>/", CommitUpdate.as_view(), name="commit-update"),
    path(
        "@<username>/<topic_permlink>/contributions/",
        Contribution.as_view(),
        name="utopic-contribution",
    ),
    path(
        "@<username>/<topic_permlink>/contributors/",
        Contributor.as_view(),
        name="utopic-contributors",
    ),
    path("<permlink>/@<username>/", DetailUserTopic.as_view(), name="detail-utopic"),
    path("utopic/<permlink>/", UpdateUTopic.as_view(), name="update-utopic"),
    path("utopic/", CreateUTopic.as_view(), name="create-utopic"),
    path("@<username>/<utopic_permlink>/issues/", IssueView.as_view(), name="issues"),
    path(
        "@<username>/<utopic_permlink>/issues/closed",
        ClosedIssueView.as_view(),
        name="close-issues",
    ),
    path(
        "@<username>/<utopic_permlink>/issues/new/",
        NewIssue.as_view(),
        name="new-issue",
    ),
    path(
        "@<username>/<utopic_permlink>/issues/<permlink>/update/",
        UpdateIssue.as_view(),
        name="update-issue",
    ),
    path(
        "@<username>/<utopic_permlink>/issues/<permlink>/",
        DetailIssue.as_view(),
        name="detail-issue",
    ),
    path(
        "@<username>/<utopic_permlink>/issues/closed/<permlink>/",
        ClosedIssue.as_view(),
        name="closed-issue",
    ),
    path(
        "@<username>/<utopic_permlink>/issues/open/<permlink>/",
        OpenIssue.as_view(),
        name="open-issue",
    ),
]
