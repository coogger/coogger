from django.db.models import GenericIPAddressField, Model


class IpModel(Model):
    ip = GenericIPAddressField(unique=True)

    def __str__(self):
        return str(self.ip)
