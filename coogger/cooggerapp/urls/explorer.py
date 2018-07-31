from django.conf.urls import url

# views
from cooggerapp.views import explorer

urlpatterns = [
    url(r'^tags/(?P<hashtag>.+)/', explorer.Hashtag.as_view(), name="hashtag"),
    url(r'^list/(?P<list_>.+)/', explorer.Userlist.as_view(), name="list"),
    url(r'^language/(?P<lang_name>.+)/', explorer.Languages.as_view(), name="language"),
    url(r'^category/(?P<cat_name>.+)/', explorer.Categories.as_view(), name="category"),
    url(r'^filter', explorer.Filter.as_view(), name="filter"),
    ]
