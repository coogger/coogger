from django.contrib.admin import site

from .models import IpModel

site.register(IpModel)
