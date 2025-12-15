#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Extrae texto del PDF de Planilla usando Google Cloud Vision
"""
import sys
import io

pdf_path = r"C:\Users\USUARIO\Downloads\DESCARGO PLANILLA 2012-12.pdf"

print("=" * 70)
print("EXTRAYENDO TEXTO DE PDF CON GOOGLE VISION")
print("=" * 70)

try:
    # Intentar con Google Cloud Vision primero
    try:
        from google.cloud import vision
        from pathlib import Path
        
        print(f"\n1. Leyendo PDF: {pdf_path}")
        
        with open(pdf_path, 'rb') as f:
            pdf_content = f.read()
        
        print(f"   ✅ PDF cargado ({len(pdf_content)} bytes)")
        
        # Crear cliente
        from utils.google_ocr import obtener_cliente_vision
        cliente = obtener_cliente_vision()
        
        if cliente:
            print(f"\n2. Enviando a Google Vision...")
            
            # Usar PDF Document Text Detection
            image = vision.Image(content=pdf_content[:4000000])  # Límite de 4MB
            
            request = vision.AnnotateImageRequest(
                image=image,
                features=[
                    vision.Feature(type_=vision.Feature.Type.DOCUMENT_TEXT_DETECTION)
                ]
            )
            
            response = cliente.annotate_image(request)
            
            if response.text_annotations:
                texto = response.text_annotations[0].description
                print(f"   ✅ Texto extraído ({len(texto)} caracteres)")
                
                print(f"\n" + "=" * 70)
                print("TEXTO EXTRAÍDO:")
                print("=" * 70)
                print(texto[:2000])
                
                # Guardar
                with open("texto_planilla_extraido.txt", "w", encoding="utf-8") as f:
                    f.write(texto)
                print(f"\n✅ Guardado en: texto_planilla_extraido.txt")
            else:
                print(f"   ❌ No se encontró texto")
        else:
            print(f"   ❌ Google Vision no configurado")
            print(f"      Coloca credentials.json en la carpeta del proyecto")
    
    except Exception as e:
        print(f"   Error Google Vision: {e}")
        print(f"\n   Intentando con PyPDF2...")
        
        try:
            from PyPDF2 import PdfReader
            
            with open(pdf_path, 'rb') as f:
                reader = PdfReader(f)
                print(f"   ✅ PDF abierto ({len(reader.pages)} páginas)")
                
                texto_completo = ""
                for i, pagina in enumerate(reader.pages[:5], 1):  # Primeras 5 páginas
                    texto = pagina.extract_text()
                    if texto:
                        texto_completo += f"\n--- PÁGINA {i} ---\n{texto}"
                
                if texto_completo.strip():
                    print(f"   ✅ Texto extraído ({len(texto_completo)} caracteres)")
                    
                    print(f"\n" + "=" * 70)
                    print("TEXTO EXTRAÍDO:")
                    print("=" * 70)
                    print(texto_completo[:2000])
                    
                    # Guardar
                    with open("texto_planilla_extraido.txt", "w", encoding="utf-8") as f:
                        f.write(texto_completo)
                    print(f"\n✅ Guardado en: texto_planilla_extraido.txt")
                else:
                    print(f"   ❌ PyPDF2 no extrajo texto (probablemente PDF con imágenes)")
        
        except Exception as e2:
            print(f"   Error PyPDF2: {e2}")

except Exception as e:
    print(f"❌ Error general: {e}")

print("\n" + "=" * 70)
print("Revisa el archivo 'texto_planilla_extraido.txt'")
print("=" * 70)
