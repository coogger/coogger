from django.conf.urls import url

#views
from apps.cooggerapp.views import signup_or_login

urlpatterns = [
    url(r"^/signup/",signup_or_login.MySignup.as_view(),name = "cooggerapp-signup"),
    url(r"^/signup-author/",signup_or_login.SingupAuthor.as_view(),name = "cooggerapp-signup_author"),
    url(r"^/login/",signup_or_login.Login.as_view(),name = "cooggerapp-login"),
    url(r"^/logout/",signup_or_login.Logout.as_view(),name = "cooggerapp-logout"),
    ]
