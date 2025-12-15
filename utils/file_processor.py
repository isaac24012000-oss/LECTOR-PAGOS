"""
Procesador de archivos
"""
from PIL import Image
import io


def procesar_archivo(archivo):
    """Procesa un archivo y lo convierte a imagen PIL"""
    try:
        imagen = Image.open(io.BytesIO(archivo.read()))
        if imagen.mode in ('RGBA', 'LA', 'P'):
            fondo = Image.new('RGB', imagen.size, (255, 255, 255))
            if imagen.mode == 'P':
                imagen = imagen.convert('RGBA')
            fondo.paste(imagen, mask=imagen.split()[-1] if imagen.mode == 'RGBA' else None)
            imagen = fondo
        elif imagen.mode != 'RGB':
            imagen = imagen.convert('RGB')
        return imagen
    except Exception as e:
        raise Exception(f"Error al procesar archivo: {str(e)}")
