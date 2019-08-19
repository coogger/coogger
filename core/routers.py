class Common:
    apps_label = None
    db_name = None

    def db_for_read(self, model, **hints):
        if model._meta.app_label in self.apps_label:
            return self.db_name
        return None

    def db_for_write(self, model, **hints):
        if model._meta.app_label in self.apps_label:
            return self.db_name
        return None

    def allow_relation(self, obj1, obj2, **hints):
        if (
            obj1._meta.app_label in self.apps_label
            or obj2._meta.app_label in self.apps_label
        ):
            return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if app_label in self.apps_label:
            return db == self.db_name
        return None


class CooggerImagesRouter(Common):
    apps_label = ["cooggerimages"]
    db_name = "coogger_images"


class DjangoIpRouter(Common):
    apps_label = ["django_page_views", "djangoip"]
    db_name = "django_ip"


class DjangoRedirect(Common):
    apps_label = ["sites", "redirects"]
    db_name = "redirect"


class DefaultRouter(Common):
    apps_label = [
        "admin",
        "auth",
        "contenttypes",
        "sessions",
        "cooggerapp",
        "github_auth",
        "django_follow_system",
        "django_vote_system",
        "django_threadedcomments_system",
        "django_bookmark",
        "djangobadge",
        "threaded_comment",
    ]
    db_name = "default"
