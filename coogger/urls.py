from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from .utils import just_redirect_by_name

# common addresses
urlpatterns = [
    path("accounts/github/", include("github_auth.urls")),
    path("follow/", include("django_follow_system.urls")),
    path("vote/", include("django_vote_system.urls")),
    path("bookmark/", include("django_bookmark.urls")),
    path("admin/", admin.site.urls),
    path("reply/", include("core.threaded_comment.urls")),
    path("privacy/", just_redirect_by_name, name="privacy"),
    path("sponsorship/", just_redirect_by_name, name="sponsorship"),
    path("settings/", include("core.cooggerapp.urls.setting")),
    path("", include("core.cooggerapp.urls.explorer")),
    path("", include("core.cooggerapp.urls.home")),
    path("", include("core.cooggerapp.urls.content")),
    path("", include("core.cooggerapp.urls.utopic")),
    path("", include("core.cooggerapp.urls.user")),
    path("", include("core.cooggerapp.urls.sitemap")),
    path("", include("cooggerimages.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
