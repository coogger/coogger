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
    # steemconnect_auth
    redirect_url = "http://127.0.0.1:8000/accounts/steemconnect/"
    ban_count = 99999
else:
    ALLOWED_HOSTS = [".coogger.com"]
    SECURE_SSL_REDIRECT = True
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    # steemconnect_auth
    redirect_url = "https://www.coogger.com/accounts/steemconnect/"
    ban_count = 40
INSTALLED_APPS = [
    # django
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # rest
    "rest_framework",
    # coogger
    "core.cooggerapp",
    "core.api",
    # 3. p
    "django_md_editor",
    "steemconnect_auth",
    "django_ban",
    "cooggerimages"
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
    # steemconnect_auth
    "steemconnect_auth.middleware.steemconnect_auth.SteemConnectAuthMiddleware",
    # coogger
    "core.cooggerapp.middleware.head.HeadMiddleware",
    "core.cooggerapp.middleware.sort.SortMiddleware",
    "core.cooggerapp.middleware.settings.SettingsMiddleware",
]
ROOT_URLCONF = "coogger.urls"
TEMPLATES = [
    dict(
        BACKEND='django.template.backends.django.DjangoTemplates',
        DIRS=[
            os.path.join(BASE_DIR, "core", "cooggerapp", "templates"),
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
        ENGINE="django.db.backends.sqlite3",
        NAME=env("DEFAULT_DB_NAME"),
    ),
    django_ban=dict(
        ENGINE="django.db.backends.sqlite3",
        NAME=env("DJANGO_BAN_DB_NAME"),
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
LANGUAGE_CODE = "en"
TIME_ZONE = "Europe/Istanbul"
USE_I18N = True
USE_L10N = True
USE_TZ = True
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
STEEMCONNECT_AUTH_CONFIGS = dict(
    redirect_url=redirect_url,
    client_id=env("CLIENT_ID"),
    app_secret=env("APP_SECRET"),
    scope="login,offline,vote,comment,delete_comment,comment_options,custom_json,claim_reward_balance",
    code=True,
    login_redirect="/",
)
DJANGO_BAN_CONFIGS = dict(
    remove_ban_by_day=7,
    increase_count_by_minute=1,
    ban_count=ban_count,
)
