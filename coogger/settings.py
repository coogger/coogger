import os

import environ

env = environ.Env(DEBUG=(bool, False))
environ.Env.read_env()
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SECRET_KEY = env("SECRET_KEY")
DEBUG = env("DEBUG")
if DEBUG:
    ALLOWED_HOSTS = ["*"]
    # github_auth
    redirect_url = "http://127.0.0.1:8000/accounts/github/login/"
else:
    ALLOWED_HOSTS = [".coogger.com"]
    SECURE_SSL_REDIRECT = True
    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
    # github_auth
    redirect_url = "https://www.coogger.com/accounts/github/login/"
INSTALLED_APPS = [
    # django default apps
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.redirects",
    "django.contrib.sites",
    # rest api
    "rest_framework",
    # to build coogger apps
    "github_auth",
    # core.apps
    "core.md_editor",
    "core.page_views",
    "core.images",
    "core.follow_system",
    "core.ip",
    "core.vote_system",
    "core.bookmark",
    "core.cooggerapp",
    "core.threaded_comment",
]
SITE_ID = 1
PAGE_SIZE = 10
REST_FRAMEWORK = dict(
    DEFAULT_PAGINATION_CLASS="rest_framework.pagination.PageNumberPagination",
    PAGE_SIZE=PAGE_SIZE,
)
MIDDLEWARE = [
    "core.ip.middleware.ip_middleware.IpMiddleware",
    # django
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "django.contrib.redirects.middleware.RedirectFallbackMiddleware",
    # coogger
    "core.cooggerapp.middleware.head.HeadMiddleware",
    "core.cooggerapp.middleware.sort.SortMiddleware",
]
ROOT_URLCONF = "coogger.urls"
TEMPLATES = [
    dict(
        BACKEND="django.template.backends.django.DjangoTemplates",
        DIRS=[],
        APP_DIRS=True,
        OPTIONS=dict(
            context_processors=[
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "django.template.context_processors.i18n",
            ]
        ),
    )
]
WSGI_APPLICATION = "coogger.wsgi.application"
DATABASES = dict(
    default=dict(ENGINE="django.db.backends.sqlite3", NAME=env("DEFAULT_DB_NAME")),
    # default=dict(
    #     ENGINE="django.db.backends.postgresql",
    #     NAME=env("DEFAULT_DB_NAME"),
    #     USER=env("DB_USER"),
    #     PASSWORD=env("DB_PASS"),
    #     HOST=env("DB_HOST"),
    #     PORT=env("DB_PORT"),
    # ),
)
AUTH_PASSWORD_VALIDATORS = []
STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "static")
MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")
LOGIN_REDIRECT_URL = "/"
LOGOUT_REDIRECT_URL = "/"
LOGIN_URL = "/accounts/github/"
# email
EMAIL_HOST = "smtp.gmail.com"
EMAIL_HOST_USER = "cooggerapp@gmail.com"
EMAIL_HOST_PASSWORD = env("EMAIL_PASSWORD")
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_USE_SSL = False
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
ugettext = lambda s: s
LANGUAGES = (
    ("tr", ugettext("Turkish")),
    ("en", ugettext("English")),
)
LANGUAGE_CODE = "tr"
LOCALE_PATHS = (os.path.join(BASE_DIR, "locale"),)
USE_I18N = True
USE_L10N = True
USE_TZ = True
# 3. part confs
MDEDITOR_CONFIGS = dict(emoji=True, html_decode="style,script")
GITHUB_AUTH = dict(
    redirect_uri=redirect_url,
    scope="user",
    client_secret=env("GITHUB_CLIENT_SECRET"),
    client_id=env("GITHUB_CLIENT_ID"),
)
USERS_PER_TOPIC = 30
