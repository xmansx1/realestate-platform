import os
from pathlib import Path
import dj_database_url
from django.contrib.messages import constants as messages
import cloudinary
import cloudinary.uploader
import cloudinary.api
import cloudinary_storage

# المسار الأساسي
BASE_DIR = Path(__file__).resolve().parent.parent

# السرية (تؤخذ من المتغير البيئي)
SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY", "insecure-key")

# التشغيل
DEBUG = os.environ.get("DEBUG", "False") == "True"

# النطاقات المسموح بها
ALLOWED_HOSTS = ['.onrender.com', '127.0.0.1', 'localhost']

# التطبيقات
INSTALLED_APPS = [
    'whitenoise.runserver_nostatic',  # لتفعيل static في الإنتاج
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'properties',
    'widget_tweaks',
    'cloudinary',
    'cloudinary_storage',
]

# الوسيطات
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # لتقديم الملفات الثابتة
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# روابط المشروع
ROOT_URLCONF = 'config.urls'

# القوالب
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
                'properties.context_processors.news_ticker',
                'properties.context_processors.footer_settings',
            ],
        },
    },
]

# التطبيق WSGI
WSGI_APPLICATION = 'config.wsgi.application'

# قاعدة البيانات
DATABASES = {
    'default': dj_database_url.config(
        default=os.environ.get("DATABASE_URL", f"sqlite:///{BASE_DIR / 'db.sqlite3'}")
    )
}

# تحقق كلمة المرور
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# اللغة والتوقيت
LANGUAGE_CODE = 'ar'
TIME_ZONE = 'Asia/Riyadh'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# الملفات الثابتة
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# ملفات الوسائط (الصور)
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# المسارات بعد الدخول والخروج
LOGIN_REDIRECT_URL = 'dashboard'
LOGOUT_REDIRECT_URL = '/'

# تنسيق الرسائل
MESSAGE_TAGS = {
    messages.DEBUG: "alert-info",
    messages.INFO: "alert-info",
    messages.SUCCESS: "alert-success",
    messages.WARNING: "alert-warning",
    messages.ERROR: "alert-danger",
}

# التخزين في Cloudinary
DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'

CLOUDINARY_STORAGE = {
    'CLOUD_NAME': os.environ.get('CLOUDINARY_CLOUD_NAME'),
    'API_KEY': os.environ.get('CLOUDINARY_API_KEY'),
    'API_SECRET': os.environ.get('CLOUDINARY_API_SECRET'),
}
