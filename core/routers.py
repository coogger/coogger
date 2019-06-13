class DBRouter:
    default_apps = [
        "admin", "auth", 
        "contenttypes", "sessions", 
        "cooggerapp", "github_auth", 
        "django_follow_system", "django_vote_system",
        "django_threadedcomments_system", "django_bookmark"
    ]
    coogger_images_app = [
        "cooggerimages"
    ]
    django_ip_apps = [
        "contenttypes", 
        "django_page_views", 
        "djangoip",
        "django_ban",
    ]

    def db_for_read(self, model, **hints):
        app_label = model._meta.app_label
        if app_label in self.default_apps:
            return "default"
        elif app_label in self.django_ip_apps:
            return "django_ip"
        elif app_label in self.coogger_images_app:
            return "coogger_images"

    def db_for_write(self, model, **hints):
        return self.db_for_read(model, **hints)

    def allow_relation(self, obj1, obj2, **hints):
        return True

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if db == "default":
            if app_label in self.default_apps:
                return True
        elif db == "django_ip":
            if app_label in self.django_ip_apps:
                return True
        elif db == "coogger_images":
            if app_label in self.coogger_images_app:
                return True
        return False