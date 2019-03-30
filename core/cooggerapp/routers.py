class DjangoBanRouter:
    def db_for_read(self, model, **hints):
        if model._meta.app_label == "django_ban":
            return "django_ban"
        return None

    def db_for_write(self, model, **hints):
        if model._meta.app_label == "django_ban":
            return "django_ban"
        return None

    def allow_relation(self, obj1, obj2, **hints):
        if obj1._state.db in "django_ban" and obj2._state.db in "django_ban":
            return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if app_label == "django_ban" and db == "django_ban":
            return True
        return None
