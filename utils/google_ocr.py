"""
Módulo para usar Google Vision API para OCR
Maneja PDF, JPG, PNG automáticamente
"""
import os
import json
from pathlib import Path
import streamlit as st


def obtener_cliente_vision():
    """
    Obtiene cliente de Google Vision
    Busca credenciales en:
    1. Variable de entorno GOOGLE_APPLICATION_CREDENTIALS
    2. Archivo credentials.json en la carpeta del proyecto
    3. Secrets de Streamlit
    """
    try:
        from google.cloud import vision
        
        # Opción 1: Variable de entorno
        if os.getenv('GOOGLE_APPLICATION_CREDENTIALS'):
            return vision.ImageAnnotatorClient()
        
        # Opción 2: Archivo local
        credentials_path = Path('credentials.json')
        if credentials_path.exists():
            os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = str(credentials_path.absolute())
            return vision.ImageAnnotatorClient()
        
        # Opción 3: Streamlit secrets
        if hasattr(st, 'secrets') and 'google_credentials' in st.secrets:
            creds_dict = st.secrets['google_credentials']
            with open('temp_credentials.json', 'w') as f:
                json.dump(creds_dict, f)
            os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = os.path.abspath('temp_credentials.json')
            return vision.ImageAnnotatorClient()
        
        return None
    
    except ImportError:
        st.error("❌ Instala: pip install google-cloud-vision")
        return None
    except Exception as e:
        st.error(f"❌ Error al configurar Google Vision: {str(e)}")
        return None


def extraer_texto_google_vision_simple(imagen_pil):
    """
    Versión simplificada para imágenes PIL
    
    Args:
        imagen_pil: Imagen PIL
    
    Returns:
        str: Texto extraído
    """
    try:
        from google.cloud import vision
        import io
        
        cliente = obtener_cliente_vision()
        if not cliente:
            return None
        
        # Convertir PIL a bytes
        buffer = io.BytesIO()
        imagen_pil.save(buffer, format='PNG')
        imagen_bytes = buffer.getvalue()
        
        # Usar Google Vision
        image = vision.Image(content=imagen_bytes)
        
        request = vision.AnnotateImageRequest(
            image=image,
            features=[
                vision.Feature(type_=vision.Feature.Type.DOCUMENT_TEXT_DETECTION)
            ]
        )
        
        response = cliente.annotate_image(request)
        
        # Extraer texto
        if response.text_annotations:
            texto = response.text_annotations[0].description
            return texto if len(texto.strip()) > 10 else None
        
        return None
    
    except Exception as e:
        return None


def verificar_credenciales():
    """
    Verifica si las credenciales de Google están configuradas
    
    Returns:
        bool: True si están configuradas
    """
    try:
        from google.cloud import vision
        
        # Intentar crear cliente
        cliente = obtener_cliente_vision()
        
        if cliente:
            return True
        
        return False
    
    except:
        return False
