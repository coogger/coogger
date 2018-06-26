from django.conf.urls import include, url

# main project = coogger
urlpatterns = [
    url(r"^post",include("cooggerapp.urls.controls")), # post
    url(r"^settings",include("cooggerapp.urls.csettings")), # settings
    url(r"^delete",include("cooggerapp.urls.delete")), # delete
    url(r"^accounts",include("cooggerapp.urls.signup_or_login")), # accounts işlemleri
    url(r"^",include("cooggerapp.urls.explorer")), # explorer
    url(r"^",include("cooggerapp.urls.home")), # home
    url(r"^",include("cooggerapp.urls.detail")), # post detail
    url(r"^",include("cooggerapp.urls.users")), # users
    url(r"^",include("cooggerapp.urls.seo")), # seo
]
