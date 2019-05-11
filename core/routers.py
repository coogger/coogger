class DBRouter:
    default_apps = [
        "admin", "auth", 
        "contenttypes", "sessions", 
        "steemconnect_auth", "cooggerapp", 
    ]
    django_ban_apps = [
        "django_ban"
    ]
    coogger_images = [
        "cooggerimages"
    ]

    def db_for_read(self, model, **hints):
        app_label = model._meta.app_label
        if app_label in self.default_apps:
            return "default"
        elif app_label in self.django_ban_apps:
            return "django_ban"
        elif app_label in self.coogger_images:
            return "coogger_images"

    def db_for_write(self, model, **hints):
        return self.db_for_read(model, **hints)

    def allow_relation(self, obj1, obj2, **hints):
        return True

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if db == "default":
            if app_label in self.default_apps:
                return True
        elif db == "django_ban":
            if app_label in self.django_ban_apps:
                return True
        elif db == "coogger_images":
            if app_label in self.coogger_images:
                return True
        return False

