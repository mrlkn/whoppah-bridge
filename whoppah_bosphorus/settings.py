"""
Django settings for whoppah_bosphorus project.

Generated by 'django-admin startproject' using Django 5.1.6.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""

import os
from pathlib import Path
import environ

# Initialize environment variables
env = environ.Env()
environ.Env.read_env()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-=2kx8*(h3lyhmffqj%q(0q5!j=z_*giem7na+5ta@*xu$xoh%$'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    # Unfold Admin Theme
    'unfold',
    'unfold.contrib.filters',  # Optional for enhanced filters
    'unfold.contrib.forms',    # Optional for enhanced forms
    
    # Django Default Apps
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # Third-party apps
    'debug_toolbar',
    
    # Project apps
    'accounts',
    'orders',
    'core',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',  # Debug Toolbar middleware
    'accounts.middleware.RoleBasedAccessMiddleware',  # Role-based access control middleware
    'accounts.middleware.ActivityTrackingMiddleware',  # User activity tracking middleware
    'core.middleware.AuditMiddleware',  # Audit trail middleware
]

ROOT_URLCONF = 'whoppah_bosphorus.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'templates'),
        ],
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

WSGI_APPLICATION = 'whoppah_bosphorus.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = env('LANGUAGE_CODE', default='en-us')

TIME_ZONE = env('TIME_ZONE', default='UTC')

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = env('STATIC_URL', default='static/')
STATIC_ROOT = BASE_DIR / env('STATIC_ROOT', default='staticfiles')
STATICFILES_DIRS = [
    BASE_DIR / 'static',
]

MEDIA_URL = env('MEDIA_URL', default='media/')
MEDIA_ROOT = BASE_DIR / env('MEDIA_ROOT', default='media')

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Custom user model
AUTH_USER_MODEL = 'accounts.User'

# Authentication backends
AUTHENTICATION_BACKENDS = [
    'accounts.backends.EmailBackend',
    'django.contrib.auth.backends.ModelBackend',
]

# Authentication Settings
LOGIN_URL = 'accounts:login'
LOGIN_REDIRECT_URL = '/'  # Redirect to home page after login
LOGOUT_REDIRECT_URL = '/'  # Redirect to home page after logout

# Email Settings (for password reset)
# For development, use console backend
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# For production, use SMTP backend (uncomment and configure for production)
# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# EMAIL_HOST = 'smtp.example.com'
# EMAIL_PORT = 587
# EMAIL_USE_TLS = True
# EMAIL_HOST_USER = 'youremail@example.com'
# EMAIL_HOST_PASSWORD = 'yourpassword'
# DEFAULT_FROM_EMAIL = 'WhoppahBridge <noreply@example.com>'

# Django Debug Toolbar Settings
INTERNAL_IPS = [
    '127.0.0.1',
    'localhost',
]

# Unfold Admin Settings
UNFOLD = {
    "SITE_TITLE": "WhoppahBridge",
    "SITE_HEADER": "WhoppahBridge",
    "SITE_SYMBOL": "move_item", # Material symbol for logistics
    "COLORS": {
        "primary": {
            "50": "230 242 237",  # Very light green
            "100": "209 232 221", # Light green
            "200": "181 218 201", # Light-medium green
            "300": "132 189 159", # Medium green
            "400": "77 153 114",  # Medium-dark green
            "500": "0 93 51",     # #005D33 - Whoppah Green
            "600": "0 81 44",     # Slightly darker
            "700": "0 70 38",     # Darker
            "800": "0 58 32",     # Even darker
            "900": "0 47 26",     # Darkest
        },
    },
    "SIDEBAR": {
        "show_search": True,
        "show_all_applications": True,
        "navigation_icon_mapping": {
            "orders": "📦",
            "accounts": "👤",
            "auth": "🔐",
            "core": "⚙️",
        },
    },
    "EXTENSIONS": {
        "modeltranslation": False,
    },
}

# Environment-specific settings
if os.environ.get('DJANGO_SETTINGS_MODULE') == 'whoppah_bosphorus.settings_prod':
    from .settings_prod import *  # noqa
else:
    from .settings_dev import *  # noqa
