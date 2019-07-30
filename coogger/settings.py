import os
import environ
env = environ.Env(
    DEBUG=(bool, False)
)
environ.Env.read_env()
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SECRET_KEY = env("SECRET_KEY")
DEBUG = env("DEBUG")
if DEBUG:
    ALLOWED_HOSTS = ["*"]
    # github_auth
    redirect_url = "http://127.0.0.1:8000/accounts/github/login/"
    ban_count = 99999
else:
    ALLOWED_HOSTS = [".coogger.com"]
    SECURE_SSL_REDIRECT = True
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    # github_auth
    redirect_url = "https://www.coogger.com/accounts/github/login/"
    ban_count = 100
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
    "django_page_views",
    "django_md_editor",
    "django_ban",
    "cooggerimages",
    "github_auth",
    "django_follow_system",
    "djangoip",
    "django_vote_system",
    "django_bookmark",
    "djangobadge",
    "core.cooggerapp",
    "core.api",
]
PAGE_SIZE = 10
REST_FRAMEWORK = dict(
    DEFAULT_PAGINATION_CLASS="rest_framework.pagination.PageNumberPagination",
    PAGE_SIZE=PAGE_SIZE,
)
MIDDLEWARE = [
    "djangoip.middleware.ip_middleware.IpMiddleware",
    # ban
    "django_ban.middleware.ip.IPBanMiddleware",
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
    "core.cooggerapp.middleware.sort.SortMiddleware",
]
ROOT_URLCONF = "coogger.urls"
TEMPLATES = [
    dict(
        BACKEND='django.template.backends.django.DjangoTemplates',
        DIRS=[],
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
        ENGINE="django.db.backends.sqlite3",
        NAME=env("DEFAULT_DB_NAME"),
    ),
    django_ip=dict(
        ENGINE="django.db.backends.sqlite3",
        NAME=env("DJANGO_IP_DB_NAME"),
    ),
    coogger_images=dict(
        ENGINE="django.db.backends.sqlite3",
        NAME=env("COOGGER_IMAGES_DB_NAME"),
    ),
)
DATABASE_ROUTERS = [
    "core.routers.DBRouter",
    ]
AUTH_PASSWORD_VALIDATORS = []
USE_I18N = True
USE_L10N = True
USE_TZ = True
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
# 3. part confs
MDEDITOR_CONFIGS = dict(
    emoji=True,
)
DJANGO_BAN_CONFIGS = dict(
    remove_ban_time=60,
    permission_second=1,
    permission_request_count=10,
)
GITHUB_AUTH = dict(
    redirect_uri=redirect_url,
    scope="user",
    client_secret=env("GITHUB_CLIENT_SECRET"),
    client_id=env("GITHUB_CLIENT_ID"),
)
