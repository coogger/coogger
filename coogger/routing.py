class GeneralRouter(object):
    def db_for_read(self, model, **hints):
        if model._meta.app_label in ["admin", "auth", "contenttypes", "cooggerapp", "sessions"]:
            return "default"
        elif model._meta.app_label == "steemitapp":
            return "steemit"

    def db_for_write(self, model, **hints):
        if model._meta.app_label in ["admin", "auth", "contenttypes", "cooggerapp", "sessions"]:
            return "default"
        elif model._meta.app_label == "steemitapp":
            return "steemit"

    def allow_relation(self, obj1, obj2, **hints):
        return True

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if db == "steemit":
            if app_label in ["admin", "auth", "contenttypes", "sessions","steemitapp"]:
                return True
            return False
        if db == "default":
            if app_label in ["admin", "auth", "contenttypes", "sessions","cooggerapp"]:
                return True
            return False
