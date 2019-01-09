from django.conf.urls import url

# views
from cooggerapp.views import explorer

urlpatterns = [
    url(r'^topic/(?P<topic>.+)/', explorer.TopicView.as_view(), name="topic"),
    url(r'^tags/(?P<hashtag>.+)/', explorer.Hashtag.as_view(), name="hashtag"),
    url(r'^language/(?P<lang_name>.+)/', explorer.Languages.as_view(), name="language"),
    url(r'^category/(?P<cat_name>.+)/', explorer.Categories.as_view(), name="category"),
    url(r'^filter', explorer.Filter.as_view(), name="filter"),
    ]

# aslında bütün keşif adreslerini filter ile yapabilirsin.
