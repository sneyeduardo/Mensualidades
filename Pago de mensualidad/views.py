from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Inscripcion, PagoMensualidad
from .configuracion.forms import PagoMensualidadForm

def registrar_pago_mensualidad(request):
    if request.method == 'POST':
        form = PagoMensualidadForm(request.POST)
        
        if form.is_valid():
            # 1. Capturamos la cédula que escribió el usuario
            cedula = form.cleaned_data.get('cedula_estudiante')
            
            try:
                # 2. Buscamos al estudiante en la base de datos de inscripciones
                # Recordando que la cédula es la Primary Key
                estudiante = Inscripcion.objects.get(cedula=cedula)
                
                # 3. Preparamos el pago, pero le decimos commit=False 
                # porque aún falta asignarle de quién es el pago
                nuevo_pago = form.save(commit=False)
                nuevo_pago.estudiante = estudiante # Asignamos la relación
                
                # 4. Ahora sí, guardamos en la base de datos
                nuevo_pago.save()
                
                messages.success(request, f'¡Pago de la {nuevo_pago.get_mes_pagado_display()} registrado con éxito para {estudiante.nombre}!')
                return redirect('ruta_de_exito') # Cambia esto por el nombre de tu URL
                
            except Inscripcion.DoesNotExist:
                # Si la cédula no existe, le mostramos un error en pantalla
                messages.error(request, 'Error: No se encontró ningún estudiante inscrito con esta cédula.')
    else:
        form = PagoMensualidadForm()

    return render(request, 'tu_app/formulario_pago.html', {'form': form})