from functools import wraps
from django.conf import settings
from django.shortcuts import render
from cooggerapp.common.utils import common_context
from social_django.utils import load_strategy
from django.contrib.auth.models import User

# models
from cooggerapp.models import OtherInformationOfUsers

def render_to(template):
    def decorator(func):
        @wraps(func)
        def wrapper(request, *args, **kwargs):
            out = func(request, *args, **kwargs) or {}
            if isinstance(out, dict):
                out = render(request, template, common_context(
                    settings.AUTHENTICATION_BACKENDS,
                    load_strategy(),
                    request.user,
                    plus_id=getattr(settings, 'SOCIAL_AUTH_GOOGLE_PLUS_KEY', None),
                    **out
                ))
            return out
        return wrapper
    return decorator
