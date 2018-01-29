from django.conf.urls import url

#views
from apps.cooggerapp.views import signup_or_login

urlpatterns = [
    url(r"^/signup/",signup_or_login.MySignupBasedClass.as_view(),name = "signup"),
    url(r"^/signup-author/",signup_or_login.SingupAuthorBasedClass.as_view(),name = "signup_author"),
    url(r"^/login/",signup_or_login.LoginBasedClass.as_view(),name = "login"),
    url(r"^/logout/",signup_or_login.LogoutBasedClass.as_view(),name = "logout"),
    ]
