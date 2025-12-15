#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Analizador de PDF de Planilla
Extrae y muestra la estructura del PDF
"""
import sys
from pathlib import Path

pdf_path = r"C:\Users\USUARIO\Downloads\DESCARGO PLANILLA 2012-12.pdf"

print("=" * 70)
print("ANALIZANDO ESTRUCTURA DEL PDF DE PLANILLA")
print("=" * 70)

try:
    from PyPDF2 import PdfReader
    
    print(f"\n1. Abriendo PDF: {pdf_path}")
    
    # Abrir PDF
    with open(pdf_path, 'rb') as f:
        reader = PdfReader(f)
        num_paginas = len(reader.pages)
        print(f"   ✅ PDF abierto ({num_paginas} páginas)")
        
        # Extraer texto de la primera página
        print(f"\n2. Extrayendo texto de página 1...")
        pagina = reader.pages[0]
        texto = pagina.extract_text()
        
        if texto and texto.strip():
            print(f"   ✅ Texto extraído ({len(texto)} caracteres)")
            
            print(f"\n" + "=" * 70)
            print("TEXTO EXTRAÍDO (primeros 2000 caracteres):")
            print("=" * 70)
            print(texto[:2000])
            
            # Guardar texto completo
            with open("texto_extraido_planilla.txt", "w", encoding="utf-8") as out_f:
                out_f.write(texto)
            print(f"\nTexto completo guardado en: texto_extraido_planilla.txt")
            
            # Análisis rápido
            print(f"\n" + "=" * 70)
            print("ANÁLISIS:")
            print("=" * 70)
            
            lineas = texto.split('\n')
            print(f"Total de líneas: {len(lineas)}")
            print(f"Primeras 20 líneas no vacías:")
            contador = 0
            for linea in lineas:
                if linea.strip() and contador < 20:
                    print(f"  {contador+1:2d}. {linea[:70]}")
                    contador += 1
        else:
            print(f"   Error: No se extrajo texto")

except FileNotFoundError:
    print(f"Error: Archivo no encontrado")

except Exception as e:
    print(f"Error: {e}")

print("\n" + "=" * 70)
print("Abre 'texto_extraido_planilla.txt' para ver el contenido completo")
print("=" * 70)
