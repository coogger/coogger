import os
import environ
env = environ.Env(
    DEBUG=(bool, False)
)
environ.Env.read_env()
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SECRET_KEY = env("SECRET_KEY")
DEBUG = env("DEBUG")
ALLOWED_HOSTS = ["*"]
INSTALLED_APPS = [
    # django
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # editor
    "django_md_editor",
    # rest
    "rest_framework",
    # steemconnect
    "steemconnect_auth",
    # coogger
    "core.cooggerapp",
    "core.api",
    # ban
    "django_ban",

]
AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
    "steemconnect_auth.auth.steemconnect.SteemConnectBackend",
]
PAGE_SIZE = 10
REST_FRAMEWORK = dict(
    DEFAULT_PAGINATION_CLASS="rest_framework.pagination.PageNumberPagination",
    PAGE_SIZE=PAGE_SIZE,
)
MIDDLEWARE = [
    # django
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    # coogger
    "core.cooggerapp.middleware.head.HeadMiddleware",
    "core.cooggerapp.middleware.general.GeneralMiddleware",
    # ban
    "django_ban.middleware.ip.IPBanMiddleware",
]
ROOT_URLCONF = "coogger.urls"
TEMPLATES = [
    dict(
        BACKEND='django.template.backends.django.DjangoTemplates',
        DIRS=[
            os.path.join(BASE_DIR, "core", "cooggerapp", "template"),
        ],
    APP_DIRS=True,
    OPTIONS=dict(
        context_processors=[
            'django.template.context_processors.debug',
            'django.template.context_processors.request',
            'django.contrib.auth.context_processors.auth',
            'django.contrib.messages.context_processors.messages',
            ],
        ),
    ),
]
WSGI_APPLICATION = "coogger.wsgi.application"
DATABASES = dict(
    default=dict(
        ENGINE=env("DATABASES_ENGINE"),
        NAME=env("DATABASES_NAME"),
    ),
)
AUTH_PASSWORD_VALIDATORS = []
LANGUAGE_CODE = "en"
TIME_ZONE = "Europe/Istanbul"
USE_I18N = True
USE_L10N = True
USE_TZ = True
# SECURE_SSL_REDIRECT = True
# SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "static")
MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")
# md eitor
MDEDITOR_CONFIGS = dict(
    toolbar=[
        "help", "info",
        "||", "preview", "watch", "fullscreen"
        ],
)
# steemconnect_auth
if DEBUG:
    redirect_url = "http://127.0.0.1:8000/accounts/steemconnect/"
else:
    redirect_url = "https://www.coogger.com/accounts/steemconnect/"
STEEMCONNECT_AUTH_CONFIGS = dict(
    redirect_url=redirect_url,
    client_id=env("CLIENT_ID"),
    app_secret=env("APP_SECRET"),
    scope="login,offline,vote,comment,delete_comment,comment_options,custom_json,claim_reward_balance",
    code=True,
    login_redirect="/",
)
