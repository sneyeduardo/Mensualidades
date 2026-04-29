from django import forms
from .models import PagoMensualidad

class PagoMensualidadForm(forms.ModelForm):
    # Campo extra que NO está directamente en el modelo de pago, 
    # pero lo necesitamos para buscar al estudiante.
    cedula_estudiante = forms.CharField(
        max_length=20, 
        label="Cédula de Identidad",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: 2133421312'})
    )

    class Meta:
        model = PagoMensualidad
        fields = ['mes_pagado', 'banco_emisor', 'referencia_pago_movil', 'monto']
        widgets = {
            'mes_pagado': forms.Select(attrs={'class': 'form-select'}),
            'banco_emisor': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: Banesco'}),
            'referencia_pago_movil': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Últimos 4 o 6 dígitos'}),
            'monto': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
        }