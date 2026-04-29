from django.shortcuts import render, redirect
from django.contrib import messages
from django.db import IntegrityError
from .models import Inscripcion
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
import base64
import random
import string
import threading
import requests

# --- 1. FUNCIÓN PARA CONVERTIR IMÁGENES ---
def imagen_a_base64(archivo):
    if archivo:
        encoded = base64.b64encode(archivo.read()).decode('utf-8')
        return f"data:{archivo.content_type};base64,{encoded}"
    return None

# --- 2. FUNCIÓN PARA GENERAR CONTRASEÑA SEGURA ---
def generar_contrasena():
    mayuscula = random.choice(string.ascii_uppercase)
    minuscula = random.choice(string.ascii_lowercase)
    numero = random.choice(string.digits)
    simbolo = random.choice("!@#$%&*")
    
    caracteres_restantes = string.ascii_letters + string.digits + "!@#$%&*"
    relleno = [random.choice(caracteres_restantes) for _ in range(4)]
    
    lista_contrasena = [mayuscula, minuscula, numero, simbolo] + relleno
    random.shuffle(lista_contrasena)
    
    return "".join(lista_contrasena)

# --- 3. FUNCIÓN PARA ENVIAR CORREO EN SEGUNDO PLANO ---
def enviar_correo_hilo(asunto, text_content, remitente, destinatario, html_content):
    try:
        msg = EmailMultiAlternatives(asunto, text_content, remitente, destinatario)
        msg.attach_alternative(html_content, "text/html")
        msg.send()
        print(f"¡Correo enviado con éxito a {destinatario[0]} en segundo plano!")
    except Exception as e:
        print(f"Error al enviar correo en segundo plano: {e}")

# =====================================================================
# VISTAS DE LA APLICACIÓN
# =====================================================================

def inicio(request):
    return render(request, 'index.html')

def registrar_inscripcion(request):
    if request.method == 'POST':
        try:
            # 1. CAPTURAMOS DATOS DE TEXTO
            prefix_crudo = request.POST.get('ci_prefix')
            tipo_documento = prefix_crudo.replace('-', '') if prefix_crudo else 'V'
            cedula = request.POST.get('cedula')
            nombres = request.POST.get('nombres')
            apellidos = request.POST.get('apellidos')
            fecha_nacimiento = request.POST.get('fecha_nacimiento')
            profesion = request.POST.get('profesion')
            direccion = request.POST.get('direccion')
            correo = request.POST.get('correo')
            telefono = request.POST.get('telefono')
            monto = request.POST.get('monto')
            referencia = request.POST.get('referencia')
            banco = request.POST.get('banco')
            fecha_pago = request.POST.get('fecha_pago') # Capturamos la nueva fecha
            
            # 2. VALIDACIONES DE CAMPOS VACÍOS
            if not cedula or not referencia or not fecha_pago:
                messages.error(request, 'La cédula, la referencia y la fecha de pago son obligatorias.')
                return redirect('registrar_alumno')
            
            # 3. VALIDACIONES ESTRICTAS (EVITAR DUPLICADOS)
            if Inscripcion.objects.filter(cedula=cedula).exists():
                messages.error(request, f'Error: La cédula {tipo_documento}-{cedula} ya está registrada.')
                return redirect('registrar_alumno')
                
            if Inscripcion.objects.filter(correo=correo).exists():
                messages.error(request, f'Error: El correo {correo} ya está en uso.')
                return redirect('registrar_alumno')
                
            if Inscripcion.objects.filter(referencia=referencia).exists():
                messages.error(request, f'Error: La referencia {referencia} ya fue procesada.')
                return redirect('registrar_alumno')

            # 4. CAPTURAMOS Y CONVERTIMOS IMÁGENES
            foto_b64 = imagen_a_base64(request.FILES.get('foto'))
            cedula_b64 = imagen_a_base64(request.FILES.get('cedula_documento'))
            pago_b64 = imagen_a_base64(request.FILES.get('comprobante_pago'))

            # 5. GENERAMOS CONTRASEÑA Y GUARDAMOS EN BASE DE DATOS
            clave_generada = generar_contrasena()

            nueva_inscripcion = Inscripcion(
                tipo_documento=tipo_documento,
                cedula=cedula,
                nombres=nombres, apellidos=apellidos,
                fecha_nacimiento=fecha_nacimiento, profesion=profesion,
                direccion=direccion, correo=correo, telefono=telefono,
                foto=foto_b64, cedula_documento=cedula_b64, comprobante_pago=pago_b64,
                monto=monto, referencia=referencia, banco=banco,
                fecha_pago=fecha_pago,
                contrasena=clave_generada
            )
            nueva_inscripcion.save()

            # --- INTEGRACIÓN CON GOOGLE SHEETS ---
            try:
                url_google_script = "https://script.google.com/macros/s/AKfycbxlBrwmCjWf9OsWXhDN2zyGTPoZoCzceTjdVwhIWWX91z0s1fIzWv1rM4LO0RCrkuet/exec"
                datos_google = {
                    'cedula': f"{tipo_documento}-{cedula}",
                    'nombres': nombres,
                    'apellidos': apellidos,
                    'correo': correo,
                    'telefono': telefono,
                    'monto': monto,
                    'referencia': referencia,
                    'banco': banco,
                    'fecha_pago': fecha_pago
                }
                requests.post(url_google_script, data=datos_google, timeout=5)
            except Exception as e:
                print(f"Error al enviar a Google Sheets: {e}")

            # 6. ENVIAMOS EL CORREO EN SEGUNDO PLANO
            try:
                protocolo = 'https' if request.is_secure() else 'http'
                dominio = f"{protocolo}://{request.get_host()}"
                
                html_content = render_to_string('correo_bienvenida.html', {
                    'alumno': nueva_inscripcion,
                    'dominio': dominio,
                    'clave': clave_generada
                })
                text_content = strip_tags(html_content) 
                asunto = 'Comprobante de Inscripción - Diplomado IA Generativa'
                remitente = settings.DEFAULT_FROM_EMAIL 
                destinatario = [correo] 
                
                hilo_correo = threading.Thread(
                    target=enviar_correo_hilo, 
                    args=(asunto, text_content, remitente, destinatario, html_content)
                )
                hilo_correo.start()
            except Exception as e:
                print(f"Error al preparar el correo: {e}")

            messages.success(request, '¡Inscripción registrada con éxito! Revisa tu correo.')
            return redirect('registrar_alumno')

        except IntegrityError:
            messages.error(request, 'Error de integridad. Verifique datos duplicados.')
            return redirect('registrar_alumno')
        except Exception as e:
            messages.error(request, f'Error: {str(e)}')
            return redirect('registrar_alumno')

    # Carga de tabla para el GET
    lista_alumnos = Inscripcion.objects.all().order_by('-fecha_registro')
    return render(request, 'bienvenida.html', {'lista_alumnos': lista_alumnos})