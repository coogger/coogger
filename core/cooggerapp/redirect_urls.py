from django.conf.urls import include, url

# main project = coogger
urlpatterns = [
    url(r"^post/", include("core.cooggerapp.urls.post")),  # post
    url(r"^settings", include("core.cooggerapp.urls.csettings")),  # settings
    url(r"^delete", include("core.cooggerapp.urls.delete")),  # delete
    url(r"^", include("core.cooggerapp.urls.explorer")),  # explorer
    url(r"^", include("core.cooggerapp.urls.home")),  # home
    url(r"^", include("core.cooggerapp.urls.detail")),  # post detail
    url(r"^", include("core.cooggerapp.urls.users")),  # users
    url(r"^", include("core.cooggerapp.urls.sitemap")),  # sitemap
]
