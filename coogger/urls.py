from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from apps.cooggerapp.views.sitemap import robots

from .utils import just_redirect_by_name

urlpatterns = [
    path("i18n/", include("django.conf.urls.i18n")),
    path("accounts/github/", include("apps.github_auth.urls")),
    path("follow/", include("apps.follow_system.urls")),
    path("vote/", include("apps.vote_system.urls")),
    path("bookmark/", include("apps.bookmark.urls")),
    path("admin/", admin.site.urls),
    path("reply/", include("apps.threaded_comment.urls")),
    path("settings/", include("apps.cooggerapp.urls.setting")),
    path("explorer/", include("apps.cooggerapp.urls.explorer")),
    path("sitemap/", include("apps.cooggerapp.urls.sitemap")),
    path("robots.txt/", robots),
    path("", include("apps.cooggerapp.urls.home")),
    path("", include("apps.cooggerapp.urls.content")),
    path("", include("apps.cooggerapp.urls.utopic")),
    path("", include("apps.cooggerapp.urls.user")),
    path("", include("apps.images.urls")),
]

flatpages = ["privacy", "sponsorship"]
for flat in flatpages:
    urlpatterns += (path(f"{flat}/", just_redirect_by_name, name=flat),)


if settings.DEBUG:
    urlpatterns += static(
        settings.STATIC_URL, document_root=settings.STATIC_ROOT
    )
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    )
