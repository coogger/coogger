from django.urls import path

from core.api.views import ListContent, ListIssue

urlpatterns = [
    path("content/", ListContent.as_view()),
    path("issue/", ListIssue.as_view()),
]
