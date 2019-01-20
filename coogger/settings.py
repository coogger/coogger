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
    #
    "cooggerapp",
    "rest",
    "steemconnect_auth",
    "django_md_editor",
    "rest_framework",
]
AUTHENTICATION_BACKENDS = [
    "steemconnect_auth.auth.steemconnect.SteemConnectBackend",
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
    ###
    "steemconnect_auth.middleware.communities.CommunitiesMiddleware",
    "cooggerapp.middleware.head.HeadMiddleware",
    "cooggerapp.middleware.general.GeneralMiddleware",
]
ROOT_URLCONF = "urls"
TEMPLATES = [
    dict(
        BACKEND='django.template.backends.django.DjangoTemplates',
        DIRS=[
            os.path.join(BASE_DIR, "coogger","cooggerapp","template"),
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
WSGI_APPLICATION = 'wsgi.application'
DATABASES = dict(
    default=dict(
        ENGINE='django.db.backends.sqlite3',
        NAME=os.path.join(BASE_DIR, 'coogger/coogger.db'),
    ),
)
AUTH_PASSWORD_VALIDATORS = [
    dict(NAME="django.contrib.auth.password_validation.UserAttributeSimilarityValidator"),
    dict(NAME="django.contrib.auth.password_validation.MinimumLengthValidator"),
    dict(NAME="django.contrib.auth.password_validation.CommonPasswordValidator"),
    dict(NAME="django.contrib.auth.password_validation.NumericPasswordValidator"),
]
LANGUAGE_CODE = "en"
TIME_ZONE = "Europe/Istanbul"
USE_I18N = True
USE_L10N = True
USE_TZ = True
# SECURE_SSL_REDIRECT = True
# SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "coogger/static")
MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "coogger/media")
# md eitor
MDEDITOR_CONFIGS = dict(
    toolbar=[
        "undo", "redo", "|",
        "help", "info",
        "||", "preview", "watch", "fullscreen"
    ],
)
