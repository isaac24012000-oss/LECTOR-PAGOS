"""
Script de debugging para probar extracción de PDF
"""
import os
import sys
from pathlib import Path

# Buscar el PDF
posibles_rutas = [
    r"C:\Users\USUARIO\Downloads\DESCARGO PLANILLA 2012-12.pdf",
    r"C:\Users\USUARIO\Desktop\DESCARGO PLANILLA 2012-12.pdf",
    r"C:\Users\USUARIO\Desktop\LECTOR DE PAGOS\DESCARGO PLANILLA 2012-12.pdf",
]

pdf_path = None
for ruta in posibles_rutas:
    if os.path.exists(ruta):
        pdf_path = ruta
        print(f"✅ PDF encontrado: {ruta}")
        break

if not pdf_path:
    print("❌ PDF NO ENCONTRADO en las ubicaciones:")
    for ruta in posibles_rutas:
        print(f"   - {ruta}")
    sys.exit(1)

# Verificar tamaño
tamaño = os.path.getsize(pdf_path)
print(f"📄 Tamaño del PDF: {tamaño} bytes")

# Prueba 1: PyPDF2
print("\n" + "="*60)
print("PRUEBA 1: PyPDF2 (texto directo)")
print("="*60)
try:
    from PyPDF2 import PdfReader
    
    with open(pdf_path, 'rb') as f:
        reader = PdfReader(f)
        num_paginas = len(reader.pages)
        print(f"📊 Total de páginas: {num_paginas}")
        
        for i, pagina in enumerate(reader.pages[:3]):  # Primeras 3 páginas
            texto = pagina.extract_text()
            print(f"\n--- Página {i+1} ---")
            print(f"Caracteres extraídos: {len(texto) if texto else 0}")
            if texto:
                print("Primeras 500 caracteres:")
                print(texto[:500])
            else:
                print("❌ Sin texto extraído")
except Exception as e:
    print(f"❌ Error con PyPDF2: {e}")

# Prueba 2: EasyOCR
print("\n" + "="*60)
print("PRUEBA 2: EasyOCR (OCR de imagen)")
print("="*60)
try:
    from pdf2image import convert_from_path
    import easyocr
    import numpy as np
    
    print("Convirtiendo PDF a imagen (página 1)...")
    imagenes = convert_from_path(pdf_path, dpi=200, first_page=1, last_page=1)
    
    if imagenes:
        print(f"✅ Imagen generada: {imagenes[0].size}")
        
        print("Ejecutando EasyOCR...")
        imagen_array = np.array(imagenes[0])
        
        reader_ocr = easyocr.Reader(['es'], gpu=False, verbose=False)
        resultado = reader_ocr.readtext(imagen_array, detail=0)
        texto_ocr = '\n'.join(resultado)
        
        print(f"✅ Caracteres extraídos por OCR: {len(texto_ocr)}")
        if texto_ocr:
            print("\nPrimeros 500 caracteres:")
            print(texto_ocr[:500])
    else:
        print("❌ No se generaron imágenes")
        
except Exception as e:
    print(f"❌ Error con EasyOCR: {e}")
    import traceback
    traceback.print_exc()

# Prueba 3: pdfplumber (alternativa)
print("\n" + "="*60)
print("PRUEBA 3: pdfplumber (alternativa)")
print("="*60)
try:
    import pdfplumber
    
    with pdfplumber.open(pdf_path) as pdf:
        print(f"📊 Total de páginas: {len(pdf.pages)}")
        
        for i, page in enumerate(pdf.pages[:3]):
            texto = page.extract_text()
            print(f"\n--- Página {i+1} ---")
            print(f"Caracteres extraídos: {len(texto) if texto else 0}")
            if texto:
                print("Primeros 500 caracteres:")
                print(texto[:500])
            else:
                print("❌ Sin texto extraído")
except ImportError:
    print("⚠️ pdfplumber no está instalado. Instálalo con: pip install pdfplumber")
except Exception as e:
    print(f"❌ Error con pdfplumber: {e}")
    import traceback
    traceback.print_exc()
