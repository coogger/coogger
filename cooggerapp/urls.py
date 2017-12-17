from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
import os
from .views import (
    controls,csettings,detail,explorer,home,signup_or_login,tools,topics,users
    )
urlpatterns = [
    url(r'^$', home.home,name = "home"),
    url(r'^search',home.search,name = "search"),
    url(r'^notification',home.notification),
    url(r'^admin/', admin.site.urls),
    url(r'^ckeditor/', include('ckeditor_uploader.urls')),

    url(r"^signup$",signup_or_login.mysignup,name = "sign_up"),
    url(r"^signup-author$",signup_or_login.signup_author,name = "signup_author"),
    url(r"^login$",signup_or_login.mylogin,name = "login"),
    url(r"^logout/$",signup_or_login.mylogout,name = "logout"),

    url(r'^stars/(?P<post_id>[0-9].*)/(?P<stars_id>[0-9])$',detail.stars),

    url(r'^robots.txt$',tools.seo),
    url(r'^sitemab.xml$',tools.seo),

    url(r'^user-upload-pp$',users.upload_pp,name="user_upload_pp"),

    url(r'^create/$',controls.create,name="create"),
    url(r'^(change/(?P<content_id>.*))',controls.change,name="change"),
    url(r'^(delete/(?P<content_id>.*))',controls.delete,name="delete"),
    url(r'^chosesub/(?P<value>.*)',controls.chose_subcategory),
    url(r'^chosecat2/(?P<value>.*)',controls.chose_category2),
    url(r'^chosenone/$',controls.chosenone),

    url(r'^(?P<blog_path>@.*/(?P<utopic>.*)/(?P<path>.*))', detail.main_detail,name = "blogs"),
    url(r'^@(?P<username>.*)/(?P<utopic>.*)', users.u_topic,name = "u-topic"),
    url(r'^@(?P<username>.*)', users.user,name = "user"),

    url(r'^tags/(?P<hashtag>.*)',explorer.hashtag,name = "hashtag"),
    url(r'^list/(?P<list>.*)',explorer.list,name = "list"),

    url(r'^comment/(?P<content_path>.*)$',detail.comment,name = "comment"),

    url(r"^settings/profile$",csettings.profile),
    url(r"^settings/$",csettings.profile),
    url(r"^settings/account$",csettings.account),
    url(r"^settings/add-address$",csettings.add_address),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
