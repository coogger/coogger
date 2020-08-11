from django.urls import path

from .views import GetVotes, IsVote, VoteView

urlpatterns = [
    path("<app_label>/<model>/<id>/", VoteView.as_view(), name="vote"),
    path("<app_label>/<model>/<id>/", GetVotes.as_view(), name="get_votes"),
    path(
        "is_vote/<username>/<app_label>/<model>/<id>/",
        IsVote.as_view(),
        name="is_vote",
    ),
]
