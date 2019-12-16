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


class ImagesRouter(Common):
    apps_label = ["images"]
    db_name = "coogger_images"


class IpRouter(Common):
    apps_label = ["page_views", "ip"]
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
        "follow_system",
        "vote_system",
        "bookmark",
        "badge",
        "threaded_comment",
    ]
    db_name = "default"
