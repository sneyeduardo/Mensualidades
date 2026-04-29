# settings.py

import os
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent.parent

# Configuración de Base de Datos para Aiven
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'defaultdb', # Nombre de la base de datos en Aiven
        'USER': 'avnadmin',
        'PASSWORD': '••••••••••••••••••••••••',
        'HOST': 'mysql-26b5007e-josemanuelyanes61-b904.g.aivencloud.com ',
        'PORT': '17223',
        'OPTIONS': {
            'ssl': {
                'ca': os.path.join(BASE_DIR, 'ca.pem'), # Ruta al certificado de Aiven
            },
        },
    }
}

# Configuración para archivos multimedia (Fotos de alumnos)
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')