from PyPDF2 import PdfReader
import re

with open(r'C:\Users\USUARIO\Downloads\DESCARGO PLANILLA 2012-12.pdf', 'rb') as f:
    reader = PdfReader(f)
    texto = reader.pages[0].extract_text()

# Buscar la tabla de afiliados
lineas = texto.split('\n')
print("TABLA DE AFILIADOS:")
print("=" * 100)
encontrado = False
for i, linea in enumerate(lineas):
    if 'CUSPP' in linea.upper() and 'Nombre' in linea:
        encontrado = True
        # Mostrar encabezados y filas
        for j in range(i, min(i+25, len(lineas))):
            print(f"{j}: {repr(lineas[j])}")
        break

if not encontrado:
    print("No encontrada")

# Buscar todas las líneas que empiezan con número de afiliado
print("\n\nAFILIADOS ENCONTRADOS:")
print("=" * 100)
patron_afiliado = r'^(\d+)\s+([0-9]{6}[A-Z]{5}\d)\s+([A-Z\s,\.]+?)(?=\s+S\s|\s+N\s)'
for linea in lineas:
    match = re.match(patron_afiliado, linea.strip())
    if match:
        print(f"Nro: {match.group(1)}, CUSPP: {match.group(2)}, Nombre: {match.group(3)}")
