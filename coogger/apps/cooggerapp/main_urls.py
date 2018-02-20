from django.conf.urls import include, url

# main project = coogger
urlpatterns = [
    url(r"^post",include("apps.cooggerapp.urls.controls")), # post
    url(r"^settings",include("apps.cooggerapp.urls.csettings")), # settings
    url(r"^delete",include("apps.cooggerapp.urls.delete")), # delete
    url(r"^explorer",include("apps.cooggerapp.urls.explorer")), # explorer
    url(r"^accounts",include("apps.cooggerapp.urls.signup_or_login")), # accounts işlemleri
    url(r"^",include("apps.cooggerapp.urls.home")), # home
    url(r"^",include("apps.cooggerapp.urls.detail")), # post detail
    url(r"^",include("apps.cooggerapp.urls.users")), # users
    url(r"^",include("apps.cooggerapp.urls.seo")), # seo
]
