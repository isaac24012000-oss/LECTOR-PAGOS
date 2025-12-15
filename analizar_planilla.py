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
        
        if texto.strip():
            print(f"   ✅ Texto extraído ({len(texto)} caracteres)")
            
            print(f"\n" + "=" * 70)
            print("TEXTO EXTRAÍDO (primeros 3000 caracteres):")
            print("=" * 70)
            print(texto[:3000])
            
            # Guardar texto completo
            with open("texto_extraido_planilla.txt", "w", encoding="utf-8") as out_f:
                out_f.write(texto)
            print(f"\n✅ Texto completo guardado en: texto_extraido_planilla.txt")
            
            # Análisis rápido
            print(f"\n" + "=" * 70)
            print("ANÁLISIS RÁPIDO:")
            print("=" * 70)
            
            lineas = texto.split('\n')
            print(f"Total de líneas: {len(lineas)}")
            print(f"\nPrimeras 20 líneas no vacías:")
            contador = 0
            for i, linea in enumerate(lineas):
                if linea.strip() and contador < 20:
                    print(f"  {contador+1:2d}. {linea[:70]}")
                    contador += 1
        else:
            print(f"   ⚠️  No se extrajo texto con PyPDF2")
            print(f"      Probablemente el PDF tiene texto incrustado como imagen")
            print(f"      Necesitaremos usar OCR (Google Vision)")

except FileNotFoundError:
    print(f"❌ Archivo no encontrado: {pdf_path}")

except Exception as e:
    print(f"❌ Error: {type(e).__name__}: {e}")

print("\n" + "=" * 70)
print("PRÓXIMOS PASOS:")
print("=" * 70)
print("""
1. Abre el archivo 'texto_extraido_planilla.txt'
2. Busca dónde están estos campos:
   - RUC
   - RAZON SOCIAL
   - PERIODO (sin " - ")
   - CUSSP
   - AFILIADO
   - FECHA DE PAGO
   - N° PLANILLA / Nro. Ticket
   - MONTO (Total Fondo Pensiones + Total Retenciones)
   
3. Comparteme el contenido para crear patrones regex exactos
