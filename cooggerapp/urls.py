from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
from cooggerapp.views import (controls,csettings,detail,explorer,home,signup_or_login,users,seo)
from django.contrib.sitemaps.views import sitemap

sitemaps = {
    "content_list":seo.ContentlistSitemap(),
    "content":seo.ContentSitemap(),
    "users":seo.UsersSitemap(),
}
urlpatterns = [
    url(r'^$', home.home,name = "home"),
    url(r'^web/search/',home.search,name = "search"),
    url(r'^web/notification/',home.notification,name = "notification"),
    url(r'^web/admin/', admin.site.urls),
    url(r'^web/ckeditor/', include('ckeditor_uploader.urls')),
    url(r"^web/signup/$",signup_or_login.mysignup,name = "signup"),
    url(r"^web/signup-author/$",signup_or_login.signup_author,name = "signup_author"),
    url(r"^web/login/$",signup_or_login.mylogin,name = "login"),
    url(r"^web/logout/$",signup_or_login.mylogout,name = "logout"),
    url(r'^robots.txt$',seo.robots),
    url(r'^web/sitemap\.xml/$', sitemap, {'sitemaps': sitemaps}),
    url(r'^web/user-upload-pp/$',users.upload_pp,name="user_upload_pp"),
    url(r'^web/create/$',controls.create,name="create"),
    url(r'^web/change/(?P<content_id>.+)/$',controls.change,name="change"),
    url(r'^web/delete/(?P<content_id>.+)/$',controls.delete,name="delete"),
    url(r'^tags/(?P<hashtag>.+)/$',explorer.hashtag,name = "hashtag"),
    url(r'^list/(?P<list_>.+)/$',explorer.users_list,name = "list"),
    url(r'^web/comment/(?P<content_path>.+)/$',detail.comment,name = "comment"),
    url(r"^web/settings/profile/$",csettings.profile,name = "sprofile"),
    url(r"^web/settings/$",csettings.profile,name  ="settings"),
    url(r"^web/settings/account/$",csettings.account,name = "saccount"),
    url(r"^web/settings/add-address/$",csettings.add_address,name = "saddaddress"),
    url(r"^web/about/(?P<username>.+)/$",users.about,name="userabout"),# kullanıcı hakkında bilgiler
    url(r"^web/following/content/$",home.following_content,name="followingcontent"), # takiplerin paylaşılan içerikleri
    url(r"^web/following/$",users.following,name="following"), # takip etme/takip bırakma
    #url(r"^web/followers/(?P<username>.+)/$",users.followers,name="followers"),
    url(r'^(?P<username>.+)/(?P<utopic>.+)/(?P<path>.+)/$', detail.main_detail,name = "detail"),
    url(r'^(?P<username>.+)/(?P<utopic>.+)/$', users.u_topic,name = "utopic"),
    url(r'^(?P<username>.+)/$', users.user,name = "user"),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
