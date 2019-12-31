from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from .utils import just_redirect_by_name

urlpatterns = [
    path("i18n/", include("django.conf.urls.i18n")),
    path("accounts/github/", include("github_auth.urls")),
    path("follow/", include("core.follow_system.urls")),
    path("vote/", include("core.vote_system.urls")),
    path("bookmark/", include("core.bookmark.urls")),
    path("admin/", admin.site.urls),
    path("reply/", include("core.threaded_comment.urls")),
    path("settings/", include("core.cooggerapp.urls.setting")),
    path("", include("core.cooggerapp.urls.explorer")),
    path("", include("core.cooggerapp.urls.home")),
    path("", include("core.cooggerapp.urls.content")),
    path("", include("core.cooggerapp.urls.utopic")),
    path("", include("core.cooggerapp.urls.user")),
    path("", include("core.cooggerapp.urls.sitemap")),
    path("", include("core.images.urls")),
]

flatpages = ["privacy", "sponsorship"]
for flat in flatpages:
    urlpatterns += (path(f"{flat}/", just_redirect_by_name, name=flat),)


if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
