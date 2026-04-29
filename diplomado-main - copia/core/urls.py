from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

# Importamos las vistas desde tu aplicación 'inscripciones'
from inscripciones import views

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # 1. Página de inicio (Tu index.html con el Login)
    path('', views.login_pagos, name='login_pagos'),
    
    # 2. Formulario de mensualidades (Tu bienvenida.html)
    path('mensualidades/', views.formulario_pago, name='formulario_pago'),
    
    # 3. Cerrar sesión
    path('salir/', views.salir, name='salir'),
    
    # 4. Ruta para el registro inicial de alumnos (Mantenida por si la necesitas)
    path('registrar/', views.registrar_inscripcion, name='registrar_alumno'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)