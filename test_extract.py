#!/usr/bin/env python
"""Script de prueba para verificar extracción de datos"""

import io
from PyPDF2 import PdfReader
import re

# Leer el PDF
with open(r'C:\Users\USUARIO\Downloads\DESCARGO PLANILLA 2012-12.pdf', 'rb') as f:
    reader = PdfReader(f)
    text = reader.pages[0].extract_text()

print('=== TEXTO EXTRAÍDO (primeros 1500 caracteres) ===')
print(text[:1500])
print('\n' + '='*60)
print('=== PRUEBA DE EXTRACCIÓN ===')
print('='*60 + '\n')

# Función de extracción
def extraer_campo(texto, patron):
    try:
        match = re.search(patron, texto, re.IGNORECASE | re.MULTILINE | re.DOTALL)
        if match:
            valor = match.group(1).strip()
            return valor if valor else "No detectado"
        return "No detectado"
    except:
        return "No detectado"

# Probar RUC
ruc = extraer_campo(text, r'RUC[:\s]+(\d{11})')
print(f'✓ RUC: {ruc}')

# Probar Razón Social
razon = extraer_campo(text, r'(?:Nombre\s+o\s+)?Razón\s+Social[:\s]+([^\n]+?)(?:\s*RUC|$)')
print(f'✓ RAZÓN SOCIAL: {razon}')

# Probar Período
periodo = extraer_campo(text, r'Periodo\s+(?:de\s+Devengue)?[:\s]+(\d{4}-\d{2})')
print(f'✓ PERIODO: {periodo}')

# Probar Planilla
planilla = extraer_campo(text, r'(?:Número\s+de\s+)?Planilla[:\s]+(\d+)')
print(f'✓ N° PLANILLA: {planilla}')

# Probar CUSSP - busca después de "CUSPP" y antes de "Nombre"
cussp = extraer_campo(text, r'CUSPP[:\s]*\n\s*([0-9A-Z]+)')
if cussp == "No detectado":
    cussp = extraer_campo(text, r'(?:CUSPP|CUSSP)[:\s]*([0-9A-Z]+)')
print(f'✓ CUSSP: {cussp}')

# Probar Afiliado - "Nro. de Afiliados Declarados"
afiliado = extraer_campo(text, r'Nro\.?\s+de\s+Afiliados?\s+Declarados[:\s]*\n?\s*(\d+)')
print(f'✓ AFILIADO: {afiliado}')

# Probar Fecha de Pago
fecha = extraer_campo(text, r'Fecha\s+de\s+Pago[:\s]*\n?\s*(\d{1,2}[/-]\d{1,2}[/-]\d{4})')
print(f'✓ FECHA DE PAGO: {fecha}')

# Probar Monto - "Total Fondo Pensiones" o "Total Retenciones y Retribuciones"
monto = extraer_campo(text, r'Total\s+Fondo\s+Pensiones[:\s]*\n?\s*(S/\.\s*[\d.,]+)')
if monto == "No detectado":
    monto = extraer_campo(text, r'Total\s+Retenciones\s+y\s+Retribuciones[:\s]*\n?\s*(S/\.\s*[\d.,]+)')
print(f'✓ MONTO: {monto}')

print('\n' + '='*60)
print('Extracción completada')
