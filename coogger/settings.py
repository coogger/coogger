# cooggerup
from steem import Steem
KEYS = [

]
STEEM = Steem(nodes=['https://api.steemit.com'],keys = KEYS)
APPROVED = """
Congratulations, your contribution has been approved.
- Your contribution type {}
------
You can contact us on [discord](https://discord.gg/q2rRY8Q).
[coogger-moderator]
"""

CAN_NOT_BE_APPROVED = """
Your contribution cannot be approved.
- Because {}
-----
You can contact us on [discord](https://discord.gg/q2rRY8Q).
[coogger-moderator]
"""
import os
AUTHENTICATION_BACKENDS = (
     'steemconnect.backends.SteemConnectOAuth2',
     'django.contrib.auth.backends.ModelBackend',
)
SOCIAL_AUTH_STEEMCONNECT_KEY = "coogger.app"
SOCIAL_AUTH_STEEMCONNECT_DEFAULT_SCOPE = ["login","vote", "comment","comment_options","custom_json","claim_reward_balance",]
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SECRET_KEY = '0o-ibh!$m!46+2y^9720!@pu(g*($hy1m0^89b%j8hrwr%k!$k'
DEBUG = True
ALLOWED_HOSTS = ["*"]
INSTALLED_APPS = [
    "djmd",
    "cooggerup",
    "api",
    "rest_framework",
    "cooggerapp",
    "social_django",
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]
ROOT_URLCONF = 'urls'
TEMPLATES = [
    {
        'BACKEND': 'django_jinja.backend.Jinja2',
        'APP_DIRS': False,
        'DIRS': [os.path.join(BASE_DIR, "coogger","cooggerapp","template","jinja")],
        'OPTIONS': {
            'match_extension': '.html',
            'match_regex': r'^(?!admin/).*',
            'filters': {
                'backend_name': 'cooggerapp.common.filters.backend_name',
                'backend_class': 'cooggerapp.common.filters.backend_class',
                'icon_name': 'cooggerapp.common.filters.icon_name',
                'social_backends': 'cooggerapp.common.filters.social_backends',
                'legacy_backends': 'cooggerapp.common.filters.legacy_backends',
                'oauth_backends': 'cooggerapp.common.filters.oauth_backends',
                'filter_backends': 'cooggerapp.common.filters.filter_backends',
                'slice_by': 'cooggerapp.common.filters.slice_by',
                'order_backends': 'cooggerapp.common.filters.order_backends'
            },
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'social_django.context_processors.backends',
                'django.template.context_processors.static',
            ],
        }
    },
    {
    'BACKEND': 'django.template.backends.django.DjangoTemplates',
    'DIRS': [
    os.path.join(BASE_DIR, "coogger","cooggerapp","template"),
    os.path.join(BASE_DIR, "coogger","cooggerup","template")
    ],
    'APP_DIRS': True,
    'OPTIONS': {
        'context_processors': [
            'django.template.context_processors.debug',
            'django.template.context_processors.request',
            'django.contrib.auth.context_processors.auth',
            'django.contrib.messages.context_processors.messages',
            'social_django.context_processors.backends',
            ],
        },
    },
]
WSGI_APPLICATION = 'wsgi.application'
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'coogger/cooggerapp/db/db'),
    },
}
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]
LANGUAGE_CODE = 'en'
TIME_ZONE = 'Europe/Istanbul'
USE_I18N = True
USE_L10N = True
USE_TZ = True
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
