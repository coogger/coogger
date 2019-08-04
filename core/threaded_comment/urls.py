from django.urls import path

from .view import ListReply, ReplyView

urlpatterns = [
    path("@<username>/<permlink>", ReplyView.as_view(), name="reply-detail"),
    path("api/", ListReply.as_view(), name="reply-api"),
]
