#django
from django.urls import path

#views
from ..views import explorer, home

urlpatterns = [
    path('explorer/posts/', home.Home.as_view(), name="explorer_posts"),
    path('topic/<permlink>/', explorer.TopicView.as_view(), name="topic"),
    path('tags/<hashtag>/', explorer.Hashtag.as_view(), name="hashtag"),
    path('language/<lang_name>/', explorer.Languages.as_view(), name="language"),
    path('category/<cat_name>/', explorer.Categories.as_view(), name="category"),
    path('filter/', explorer.Filter.as_view(), name="filter"),
    ]
