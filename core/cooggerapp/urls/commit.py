from django.urls import path

from ..views.commit import CommitDetail, Commits

urlpatterns = [
    path("@<username>/<topic_permlink>/commits/", Commits.as_view(), name="commits"),
    path(
        "@<username>/<topic_permlink>/commit/<hash>/",
        CommitDetail.as_view(),
        name="commit",
    ),
]
