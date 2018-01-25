#django
from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.contrib.auth.decorators import login_required

#views
from cooggerapp.views import (controls,csettings,detail,explorer,home,signup_or_login,users,seo,delete)
from cooggerapp.views import controls

urlpatterns = [
    url(r'^$', home.HomeBasedClass.as_view(),name = "home"),
    url(r'^web/search/$',home.SearchBasedClass.as_view(),name = "search"),
    url(r'^web/report/$',home.ReportBasedClass.as_view(),name = "report"),
    url(r'^web/notification/',home.NotificationBasedClass.as_view(),name = "notification"),
    url(r'^web/admin/', admin.site.urls),
    url(r'^web/ckeditor/', include('ckeditor_uploader.urls')),
    url(r"^accounts/signup/$",signup_or_login.MySignupBasedClass.as_view(),name = "signup"),
    url(r"^accounts/signup-author/$",signup_or_login.SingupAuthorBasedClass.as_view(),name = "signup_author"),
    url(r"^accounts/login/$",signup_or_login.LoginBasedClass.as_view(),name = "login"),
    url(r"^accounts/logout/$",signup_or_login.LogoutBasedClass.as_view(),name = "logout"),
    url(r'^robots.txt$',seo.robots),
    url(r'^web/sitemap-contentlist\.xml/$', sitemap, {'sitemaps': {"content_list":seo.ContentlistSitemap()}}),
    url(r'^web/sitemap-conten\.xml/$', sitemap, {'sitemaps': {"content":seo.ContentSitemap()}}),
    url(r'^web/sitemap-users\.xml/$', sitemap, {'sitemaps': {"users":seo.UsersSitemap()}}),
    url(r'^web/user-upload-pp/$',users.UploadppBasedClass.as_view(),name="user_upload_pp"),
    url(r'^web/create/$',controls.CreateBasedClass.as_view(),name="create"),
    url(r'^web/change/(?P<content_id>.+)/$',controls.ChangeBasedClass.as_view(),name="change"),
    url(r'^web/delete/address/$',delete.AddressBasedClass.as_view(),name="address_del"),
    url(r'^web/delete/(?P<content_id>.+)/$',delete.ContentBasedClass.as_view(),name="content_del"),
    url(r'^tags/(?P<hashtag>.+)/$',explorer.HashtagBasedClass.as_view(),name = "hashtag"),
    url(r'^list/(?P<list_>.+)/$',explorer.UserlistBasedClass.as_view(),name = "list"),
    url(r'^web/comment/$',detail.CommentBasedClass.as_view(),name = "comment"),
    url(r"^web/settings/profile/$",csettings.ProfileBasedClass.as_view(),name = "sprofile"),
    url(r"^web/settings/$",csettings.ProfileBasedClass.as_view(),name  ="settings"),
    url(r"^web/settings/account/$",csettings.AccountBasedClass.as_view(),name = "saccount"),
    url(r"^web/settings/add-address/$",csettings.AddaddessBasedClass.as_view(),name = "saddaddress"),
    url(r"^web/about/(?P<username>.+)/$",users.UserAboutBaseClass.as_view(),name="userabout"),# kullanıcı hakkında bilgiler
    url(r"^web/following/content/$",home.FollowingContentBasedClass.as_view(),name="followingcontent"), # takiplerin paylaşılan içerikleri
    url(r"^web/following/$",users.FollowBaseClass.as_view(),name="following"), # takip etme/takip bırakma
    url(r'^(?P<username>.+)/(?P<utopic>.+)/(?P<path>.+)/$', detail.DetailBasedClass.as_view(),name = "detail"),
    url(r'^(?P<username>.+)/(?P<utopic>.+)/$', users.UserTopicBasedClass.as_view(),name = "utopic"),
    url(r'^(?P<username>.+)/$', users.UserBasedClass.as_view(),name = "user"),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
