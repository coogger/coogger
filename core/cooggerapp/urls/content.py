from django.urls import path

from ..views.content import (
    Contribute, Create, Detail, Embed, TreeDetail, Update
)

urlpatterns = [
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
]
