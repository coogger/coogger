from django.conf.urls import url
from .views import home
from .views import signup_or_login
from .views import admin


# bunların sonundaki name etiketi template içinde ulaşmak istediğimizde ulaşabiliriz
#mesela name="listen" dedğimizde {% url "listen" %} şeklinde alabiliyoruz

urlpatterns = [
    url(r'^$', home.home,name = "home"),
    url(r"^signup$",signup_or_login.signup,name = "sign_up"),
    url(r"^login$",signup_or_login.mylogin,name = "login"),
    url(r'^chose-branch/(?P<value>.*)',admin.chose_branch),
] 




"""
url(r'^login$', logsign.mylogin,name="login"),
url(r'^listen/(?P<url>.*)',listen.listen),
    """