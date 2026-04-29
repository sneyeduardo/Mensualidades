"""
Django settings for core project.
"""

import os
from pathlib import Path

# Construye las rutas dentro del proyecto así: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: ¡Mantén la clave secreta en secreto en producción!
# (Django genera una por defecto, si no la tienes, puedes dejar esta por ahora en desarrollo)
SECRET_KEY = 'django-insecure-!k5+*g&z8^k#3)q@7l*4m%p1w_v(d9b$2x^r&y-c5f_h*t@j#n'

# SECURITY WARNING: no ejecutes con debug encendido en producción.
DEBUG = True

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'inscripciones',  # <-- ¡Asegúrate de tener esta línea!
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
]

ROOT_URLCONF = 'core.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        # Configuración para que Django lea tus HTML
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

WSGI_APPLICATION = 'core.wsgi.application'


# Base de datos conectada a Aiven
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'defaultdb', 
        'USER': 'avnadmin',
        'PASSWORD': 'AVNS_vIkgPXLcFad6n65he4x', # <- RECUERDA PONER LA CONTRASEÑA REAL AQUÍ
        'HOST': 'mysql-26b5007e-josemanuelyanes61-b904.g.aivencloud.com',
        'PORT': '17223',
        'OPTIONS': {
            'ssl': {
                'ca': os.path.join(BASE_DIR, 'ca.pem'),
            },
        },
    }
}


# Password validation
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
LANGUAGE_CODE = 'es-ve' # Español de Venezuela
TIME_ZONE = 'America/Caracas' # Zona horaria ajustada

USE_I18N = True
USE_TZ = True


# Configuración para archivos estáticos (CSS, JS, Imágenes del diseño)
STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
# Configuración para archivos multimedia (Fotos subidas por los alumnos)
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'



# Usamos os.environ.get para proteger las credenciales en Render
# --- CONFIGURACIÓN DE CORREOS (GMAIL - VERSIÓN SSL) ---
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 465
EMAIL_USE_SSL = True



EMAIL_HOST_USER = 'sneyeduardo4@gmail.com' # Pon el tuyo
EMAIL_HOST_PASSWORD = 'lljmzsgkrqubjpef'
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER