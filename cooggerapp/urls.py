from django.conf.urls import include, url
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings
from .views import home
from .views import signup_or_login
from .views import admin as myadmin
from .views import detail
from .views import users

urlpatterns = [
    url(r'^$', home.home,name = "home"),
    url(r'^admin/', admin.site.urls),
    url(r'^ckeditor/', include('ckeditor_uploader.urls')),
    url(r'^blogs/(?P<blog_path>.*)', detail.main_detail,name = "blogs"),
    url(r"^signup$",signup_or_login.mysignup,name = "sign_up"),
    url(r"^signup-author$",signup_or_login.signup_author,name = "signup_author"),
    url(r"^login$",signup_or_login.mylogin,name = "login"),
    url(r"^logout$",signup_or_login.mylogout,name = "logout"),
    url(r'^chosesub/(?P<value>.*)',myadmin.chose_subcategory),
    url(r'^chosecat2/(?P<value>.*)',myadmin.chose_category2),
    url(r'^chosenone/',myadmin.chosenone),
    url(r'^@(?P<username>.*)', users.user,name = "user"),
] + static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
