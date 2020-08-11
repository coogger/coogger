from django.urls import path

from .view import ListReply, ReplyUpdateView, ReplyView

urlpatterns = [
    path("@<username>/<permlink>", ReplyView.as_view(), name="reply-detail"),
    path(
        "update/@<username>/<permlink>",
        ReplyUpdateView.as_view(),
        name="reply-update",
    ),
    path("api/", ListReply.as_view(), name="reply-api"),
]
