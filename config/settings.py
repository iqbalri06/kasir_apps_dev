from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'your-secret-key-here'

DEBUG = True

ALLOWED_HOSTS = []

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'simple_shop',
    'django.contrib.humanize',
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

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            BASE_DIR / 'simple_shop' / 'templates',
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

WSGI_APPLICATION = 'config.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

AUTH_USER_MODEL = 'simple_shop.User'

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Jakarta'  # Adjust to your timezone
USE_I18N = True
USE_TZ = True

STATIC_URL = 'static/'
STATICFILES_DIRS = [
    BASE_DIR / "simple_shop" / "static",
]

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Menambahkan konfigurasi yang lebih deskriptif untuk aplikasi
SHOP_NAME = 'IQMart'
SHOP_DESCRIPTION = 'Pelanggan senang kami bahagia!'
SHOP_CONTACT_EMAIL = 'support@iqmart.com'

# Konfigurasi email di bagian bawah file

# Konfigurasi SMTP untuk Gmail
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'iqbalroudatul@gmail.com'  # Ganti dengan email Gmail Anda
EMAIL_HOST_PASSWORD = 'swnm ijap aatv kysg'  # Ganti dengan App Password Gmail Anda
DEFAULT_FROM_EMAIL = 'IQMart <iqbalroudatul@gmail.com>'
