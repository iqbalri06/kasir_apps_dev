"""
Django settings for simple_shop project.
"""
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'your-secret-key-here'

DEBUG = False

ALLOWED_HOSTS = ['.vercel.app', '.now.sh', 'localhost', '127.0.0.1']

INSTALLED_APPS = [
    'simple_shop.apps.SimpleShopConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',  # Ensure this is added
]

AUTH_USER_MODEL = 'simple_shop.User'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'simple_shop.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'simple_shop' / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'libraries': {
                'currency': 'simple_shop.templatetags.currency',
            },
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'simple_shop.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
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

LANGUAGE_CODE = 'id'
TIME_ZONE = 'Asia/Jakarta'

USE_I18N = True
USE_L10N = True
USE_TZ = True

THOUSAND_SEPARATOR = '.'
USE_THOUSAND_SEPARATOR = True
DECIMAL_SEPARATOR = ','
NUMBER_GROUPING = 3

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

STATICFILES_DIRS = [
    BASE_DIR / 'simple_shop' / 'static',
]

# Media files configuration
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Only create media directory if not on Vercel
if not os.environ.get('VERCEL'):
    os.makedirs(MEDIA_ROOT, exist_ok=True)

# QRIS Image Path (using jpg)
QRIS_IMAGE_PATH = BASE_DIR / 'simple_shop' / 'images' / 'qris.jpg'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Authentication settings
LOGIN_URL = 'simple_shop:login'
LOGIN_REDIRECT_URL = 'simple_shop:dashboard'
LOGOUT_REDIRECT_URL = 'simple_shop:login'

# Vercel-specific settings
if os.environ.get('VERCEL'):
    DEBUG = False
    ALLOWED_HOSTS = ['*']
    
    # Minimal database config
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': '/tmp/db.sqlite3',
        }
    }
    
    # Minimal middleware
    MIDDLEWARE = [
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.middleware.common.CommonMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
    ]
    
    # Basic static files
    STATIC_URL = '/static/'
    STATIC_ROOT = '/tmp/static'
    
    # Essential apps only
    INSTALLED_APPS = [
        'simple_shop.apps.SimpleShopConfig',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.staticfiles',
    ]

    # Disable media handling
    MEDIA_URL = None
    MEDIA_ROOT = None

# Disable QRIS image path in Vercel
if not os.environ.get('VERCEL'):
    QRIS_IMAGE_PATH = BASE_DIR / 'simple_shop' / 'images' / 'qris.jpg'