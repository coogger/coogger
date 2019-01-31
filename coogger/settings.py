import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SECRET_KEY = '0o-ibh!$m!46+2y^9720!@pu(g*($hy1m0^89b%j8hrwr%k!$k'
DEBUG = True
PAGE_SIZE = 10
ALLOWED_HOSTS = ["*"]
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    "django_md_editor",
    "rest_framework",
    "core.cooggerapp",
    "core.api",
    "core.steemconnect_auth",
]
AUTHENTICATION_BACKENDS = [
    "core.steemconnect_auth.auth.steemconnect.SteemConnectBackend",
    "django.contrib.auth.backends.ModelBackend",
]
REST_FRAMEWORK = dict(
    DEFAULT_PAGINATION_CLASS="rest_framework.pagination.PageNumberPagination",
    PAGE_SIZE=PAGE_SIZE,
)
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    "core.steemconnect_auth.middleware.communities.CommunitiesMiddleware",
    "core.cooggerapp.middleware.head.HeadMiddleware",
    "core.cooggerapp.middleware.general.GeneralMiddleware",
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
        ENGINE='django.db.backends.sqlite3',
        NAME=os.path.join(BASE_DIR, 'db/coogger.db'),
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
        "undo", "redo", "|",
        "bold", "del", "italic", "quote", "ucwords", "uppercase", "lowercase", "|",
        "h1", "h2", "h3", "h5", "h6", "|",
        "list-ul", "list-ol", "hr", "|",
        "link", "reference-link", "image", "code", "preformatted-text", "code-block", "table", "datetime",
        "emoji", "html-entities", "pagebreak", "goto-line", "|",
        "help", "info",
        "||", "preview", "watch", "fullscreen"
        ],
)
