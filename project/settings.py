from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent


def env(key, default=''):
    return os.environ.get(key, default)


def env_bool(key, default='false'):
    return env(key, default).lower() in ('true', '1', 'yes')


def env_int(key, default='0'):
    value = env(key, default)
    return int(value) if value.isdigit() else 0


def env_list(key, default='', separator='|'):
    value = env(key, default)
    return [v for v in value.split(separator) if v] if value else []


# Core
SECRET_KEY = env('SECRET_KEY', 'change-me-in-production')
DEBUG = env_bool('DEBUG', 'true')
ALLOWED_HOSTS = env_list('ALLOWED_HOSTS', 'localhost')
CSRF_TRUSTED_ORIGINS = env_list('CSRF_TRUSTED_ORIGINS')

# Security
SESSION_COOKIE_SECURE = env_bool('SESSION_COOKIE_SECURE')
CSRF_COOKIE_SECURE = env_bool('CSRF_COOKIE_SECURE')
SECURE_SSL_REDIRECT = env_bool('SECURE_SSL_REDIRECT')
SECURE_HSTS_SECONDS = env_int('SECURE_HSTS_SECONDS')
SECURE_HSTS_PRELOAD = env_bool('SECURE_HSTS_PRELOAD')
SECURE_HSTS_INCLUDE_SUBDOMAINS = env_bool('SECURE_HSTS_INCLUDE_SUBDOMAINS')

# ReCAPTCHA
RECAPTCHA_PUBLIC_KEY = env('RECAPTCHA_PUBLIC_KEY')
RECAPTCHA_PRIVATE_KEY = env('RECAPTCHA_PRIVATE_KEY')

INSTALLED_APPS = [
    'admin_interface',
    'colorfield',

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.postgres',
    'django.contrib.humanize',

    'django_better_admin_arrayfield',
    'django_user_agents',
    'django_recaptcha',
    'crispy_forms',
    'crispy_bootstrap5',

    'project.home',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django_user_agents.middleware.UserAgentMiddleware',
]

ROOT_URLCONF = 'project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'project.wsgi.application'

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': env('POSTGRES_DBNAME', 'personal_website'),
        'USER': env('POSTGRES_USER', 'faiz_admin'),
        'PASSWORD': env('POSTGRES_PASS', ''),
        'HOST': env('PG_HOST', '127.0.0.1'),
        'PORT': env_int('PG_PORT', '5432'),
    }
}

# Logging — stdout for Docker
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s',
            'datefmt': '%d/%b/%Y %H:%M:%S',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False,
        },
    },
}

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# i18n
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Jakarta'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Static & media
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles/')
STATICFILES_DIRS = (os.path.join(BASE_DIR, 'static/'),)
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

STORAGES = {
    'staticfiles': {
        'BACKEND': 'whitenoise.storage.CompressedStaticFilesStorage',
    },
}

# Email
EMAIL_BACKEND = env('EMAIL_BACKEND', 'django.core.mail.backends.smtp.EmailBackend')
EMAIL_HOST = env('EMAIL_HOST', 'smtp.gmail.com')
EMAIL_PORT = env_int('EMAIL_PORT', '587')
EMAIL_USE_TLS = env_bool('EMAIL_USE_TLS', 'true')
EMAIL_HOST_USER = env('EMAIL_HOST_USER', '')
EMAIL_HOST_PASSWORD = env('EMAIL_HOST_PASSWORD', '')

# Crispy Forms
CRISPY_ALLOWED_TEMPLATE_PACKS = 'bootstrap5'
CRISPY_TEMPLATE_PACK = 'bootstrap5'
