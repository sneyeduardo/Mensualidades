from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

# Importamos las DOS funciones
from inscripciones.views import inicio, registrar_inscripcion 

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Ruta 1: Cuando entran a la página principal (index.html)
    path('', inicio, name='inicio'),
    
    # Ruta 2: Cuando le dan clic a "Iniciar Inscripción" (bienvenida.html)
    path('registrar/', registrar_inscripcion, name='registrar_alumno'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)