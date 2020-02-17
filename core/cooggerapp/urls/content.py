from django.urls import path

from ..views.content import (
    ApproveContribute, Contribute, Create, Detail, Embed, RejectContribute,
    TreeDetail, Update, ReplaceOrder
)

urlpatterns = [
    path(
        "content-replace-order",
        ReplaceOrder.as_view(),
        name="contet-replace-order",
    ),
    path("embed/@<username>/<permlink>/", Embed.as_view(), name="embed"),
    path("@<username>/<permlink>/", Detail.as_view(), name="content-detail"),
    path(
        "@<username>/<topic_permlink>/tree/<hash>/",
        TreeDetail.as_view(),
        name="tree-detail",
    ),
    path("post/create/<utopic_permlink>/", Create.as_view(), name="create"),
    path("post/update/@<username>/<permlink>/", Update.as_view(), name="update"),
    path(
        "post/contribute/@<username>/<permlink>/",
        Contribute.as_view(),
        name="content-contribute",
    ),
    path(
        "@<username>/<topic_permlink>/commit/approved/<hash>/",
        ApproveContribute.as_view(),
        name="approved-contribute",
    ),
    path(
        "@<username>/<topic_permlink>/commit/rejected/<hash>/",
        RejectContribute.as_view(),
        name="rejected-contribute",
    ),

]
