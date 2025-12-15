"""
Módulo para leer y validar datos desde archivos Excel locales o GitHub
"""
import pandas as pd
import os
from difflib import SequenceMatcher
from pathlib import Path
import io
import requests

# URLs de GitHub (cambia estas URLs según tu repositorio)
GITHUB_RAW_URL = "https://raw.githubusercontent.com"
# Formato: https://raw.githubusercontent.com/tu-usuario/tu-repo/branch/LECTOR-PAGOS/archivo.xlsx
# Ejemplo: https://raw.githubusercontent.com/usuario/lector-pagos/main/LECTOR-PAGOS/DETALLE%20AFILIADOS%20REDIRECCIONAMIENTO.xlsx

def obtener_rutas_bases():
    """Busca los archivos de bases en diferentes ubicaciones posibles"""
    posibles_rutas = [
        # Rutas para desarrollo local
        r"C:\Users\USUARIO\Desktop\LECTOR DE PAGOS\LECTOR-PAGOS\DETALLE AFILIADOS REDIRECCIONAMIENTO.xlsx",
        # Rutas relativas para Streamlit Cloud (raíz del repositorio)
        "LECTOR-PAGOS/DETALLE AFILIADOS REDIRECCIONAMIENTO.xlsx",
        "./LECTOR-PAGOS/DETALLE AFILIADOS REDIRECCIONAMIENTO.xlsx",
        # Carpeta actual
        "DETALLE AFILIADOS REDIRECCIONAMIENTO.xlsx",
    ]
    
    redi_path = None
    pres_path = None
    
    for ruta in posibles_rutas:
        if os.path.exists(ruta):
            redi_path = ruta
            # Obtener la carpeta base para buscar PRESUNTA
            carpeta_base = os.path.dirname(ruta)
            pres_ruta = os.path.join(carpeta_base, "DETALLE AFILIADOS PRESUNTA.xlsx")
            if os.path.exists(pres_ruta):
                pres_path = pres_ruta
            break
    
    return redi_path, pres_path


def descargar_desde_github(url_github):
    """Descarga un archivo Excel desde GitHub y lo retorna como DataFrame"""
    try:
        response = requests.get(url_github, timeout=10)
        response.raise_for_status()
        return pd.read_excel(io.BytesIO(response.content))
    except Exception as e:
        print(f"Error descargando desde GitHub ({url_github}): {e}")
        return None


BASE_REDIRECCIONAMIENTO, BASE_PRESUNTA = obtener_rutas_bases()

# URLs de GitHub - Configura estas variables en Streamlit Cloud Secrets
# En Streamlit Cloud: Settings → Secrets → Añade:
# GITHUB_REDI_URL = "https://raw.githubusercontent.com/TU_USUARIO/TU_REPO/main/LECTOR-PAGOS/DETALLE%20AFILIADOS%20REDIRECCIONAMIENTO.xlsx"
# GITHUB_PRES_URL = "https://raw.githubusercontent.com/TU_USUARIO/TU_REPO/main/LECTOR-PAGOS/DETALLE%20AFILIADOS%20PRESUNTA.xlsx"

GITHUB_REDI_DEFAULT = os.environ.get(
    'GITHUB_REDI_URL',
    None  # Se llenará dinámicamente o usará rutas locales
)
GITHUB_PRES_DEFAULT = os.environ.get(
    'GITHUB_PRES_URL',
    None  # Se llenará dinámicamente o usará rutas locales
)

# Rutas locales como fallback final (solo si GitHub falla)
if not BASE_REDIRECCIONAMIENTO:
    BASE_REDIRECCIONAMIENTO = r"C:\Users\USUARIO\Desktop\LECTOR DE PAGOS\LECTOR-PAGOS\DETALLE AFILIADOS REDIRECCIONAMIENTO.xlsx"
if not BASE_PRESUNTA:
    BASE_PRESUNTA = r"C:\Users\USUARIO\Desktop\LECTOR DE PAGOS\LECTOR-PAGOS\DETALLE AFILIADOS PRESUNTA.xlsx"


def cargar_bases_locales():
    """
    Carga los archivos Excel de bases locales de forma optimizada
    Intenta cargar desde rutas LOCALES PRIMERO (más rápido), luego GitHub como fallback
    """
    bases = {}
    
    # ========== REDIRECCIONAMIENTO ==========
    df_redi = None
    
    # Intentar PRIMERO desde rutas locales (es lo más rápido y confiable)
    if BASE_REDIRECCIONAMIENTO and os.path.exists(BASE_REDIRECCIONAMIENTO):
        try:
            df_redi = pd.read_excel(BASE_REDIRECCIONAMIENTO, dtype={
                'DOCUMENTO': str,
                'PERIODO': str,
                'CUSSP': str,
                'AFILIADO': str
            })
            print(f"✅ REDIRECCIONAMIENTO cargado localmente")
        except Exception as e:
            print(f"⚠️ Error cargando REDIRECCIONAMIENTO localmente: {e}")
    
    # Si falló localmente, intentar desde GitHub (solo si tenemos URL)
    if df_redi is None and GITHUB_REDI_DEFAULT:
        print(f"📥 Intentando cargar REDIRECCIONAMIENTO desde GitHub...")
        df_redi = descargar_desde_github(GITHUB_REDI_DEFAULT)
        if df_redi is not None:
            print(f"✅ REDIRECCIONAMIENTO cargado desde GitHub")
        else:
            print(f"⚠️ No se pudo cargar REDIRECCIONAMIENTO de GitHub")
    
    # Procesar REDIRECCIONAMIENTO si se cargó
    if df_redi is not None:
        try:
            # Limpiar espacios en blanco de forma más eficiente
            df_redi['DOCUMENTO'] = df_redi['DOCUMENTO'].astype(str).str.strip()
            df_redi['PERIODO'] = df_redi['PERIODO'].astype(str).str.strip()
            df_redi['CUSSP'] = df_redi['CUSSP'].astype(str).str.strip()
            df_redi['AFILIADO'] = df_redi['AFILIADO'].astype(str).str.strip()
            
            # Crear índice compuesto para búsquedas rápidas
            df_redi['_doc_per'] = df_redi['DOCUMENTO'] + '|' + df_redi['PERIODO']
            df_redi.set_index('_doc_per', drop=False, inplace=True)
            
            bases['REDIRECCIONAMIENTO'] = df_redi
            print(f"📊 REDIRECCIONAMIENTO: {len(df_redi)} registros cargados")
        except Exception as e:
            print(f"❌ Error procesando REDIRECCIONAMIENTO: {e}")
    else:
        print("❌ No se pudo cargar REDIRECCIONAMIENTO de ninguna fuente")
    
    # ========== PRESUNTA ==========
    df_pres = None
    
    # Intentar PRIMERO desde rutas locales (es lo más rápido y confiable)
    if BASE_PRESUNTA and os.path.exists(BASE_PRESUNTA):
        try:
            df_pres = pd.read_excel(BASE_PRESUNTA, dtype={
                'DOCUMENTO': str,
                'PERIODO': str,
                'CUSSP': str,
                'AFILIADO': str
            })
            print(f"✅ PRESUNTA cargado localmente")
        except Exception as e:
            print(f"⚠️ Error cargando PRESUNTA localmente: {e}")
    
    # Si falló localmente, intentar desde GitHub (solo si tenemos URL)
    if df_pres is None and GITHUB_PRES_DEFAULT:
        print(f"📥 Intentando cargar PRESUNTA desde GitHub...")
        df_pres = descargar_desde_github(GITHUB_PRES_DEFAULT)
        if df_pres is not None:
            print(f"✅ PRESUNTA cargado desde GitHub")
        else:
            print(f"⚠️ No se pudo cargar PRESUNTA de GitHub")
    
    # Procesar PRESUNTA si se cargó
    if df_pres is not None:
        try:
            df_pres['DOCUMENTO'] = df_pres['DOCUMENTO'].astype(str).str.strip()
            df_pres['PERIODO'] = df_pres['PERIODO'].astype(str).str.strip()
            df_pres['CUSSP'] = df_pres['CUSSP'].astype(str).str.strip()
            df_pres['AFILIADO'] = df_pres['AFILIADO'].astype(str).str.strip()
            
            # Crear índice compuesto para búsquedas rápidas
            df_pres['_doc_per'] = df_pres['DOCUMENTO'] + '|' + df_pres['PERIODO']
            df_pres.set_index('_doc_per', drop=False, inplace=True)
            
            bases['PRESUNTA'] = df_pres
            print(f"📊 PRESUNTA: {len(df_pres)} registros cargados")
        except Exception as e:
            print(f"❌ Error procesando PRESUNTA: {e}")
    else:
        print("❌ No se pudo cargar PRESUNTA de ninguna fuente")
    
    return bases


def calcular_similitud(str1, str2):
    """Calcula la similitud entre dos strings (0-1)"""
    if not str1 or not str2:
        return 0
    return SequenceMatcher(None, str1.upper(), str2.upper()).ratio()


def buscar_en_base(ruc, documento, periodo, cussp, afiliado_pdf, bases):
    """
    Busca datos en las bases locales y valida de forma optimizada
    
    Args:
        ruc: RUC del empleador
        documento: Documento (RUC del empleador)
        periodo: Período (ej: 201212)
        cussp: CUSSP del afiliado (del PDF) - puede estar vacío para fallback
        afiliado_pdf: Nombre del afiliado (del PDF) - puede estar vacío para fallback
        bases: Diccionario con DataFrames cargados
    
    Returns:
        Si viene con datos del PDF: diccionario único con validación
        Si viene del fallback (sin datos): dict con 'encontrado' y 'afiliados' (lista)
    """
    
    if not bases:
        return {'encontrado': False, 'afiliados': []}
    
    # Limpiar documento para búsqueda
    documento_busca = str(documento).strip() if documento else str(ruc).strip()
    periodo_busca = str(periodo).strip()
    cussp_busca = str(cussp).strip() if cussp and cussp != "No detectado" else ""
    afiliado_busca = str(afiliado_pdf).strip() if afiliado_pdf and afiliado_pdf != "No detectado" else ""
    
    es_fallback = not cussp_busca and not afiliado_busca
    
    # Clave de búsqueda rápida usando índice
    clave_busca = f"{documento_busca}|{periodo_busca}"
    
    # Buscar en REDIRECCIONAMIENTO primero
    if 'REDIRECCIONAMIENTO' in bases:
        df = bases['REDIRECCIONAMIENTO']
        
        # Búsqueda rápida usando el índice
        try:
            resultados_filtro = df.loc[[clave_busca]] if clave_busca in df.index else df[df['_doc_per'] == clave_busca]
        except:
            resultados_filtro = df[df['_doc_per'] == clave_busca]
        
        # Si tenemos CUSSP, filtrar también por eso
        if cussp_busca and not resultados_filtro.empty:
            resultados_filtro = resultados_filtro[resultados_filtro['CUSSP'] == cussp_busca]
        
        if not resultados_filtro.empty:
            if es_fallback:
                # Modo fallback: retornar TODOS los afiliados encontrados
                afiliados = []
                for _, fila in resultados_filtro.iterrows():
                    afiliados.append({
                        'cussp': str(fila['CUSSP']).strip(),
                        'afiliado': str(fila['AFILIADO']).strip(),
                        'origen': 'REDIRECCIONAMIENTO',
                        'observacion': f"Datos de base local (REDIRECCIONAMIENTO)"
                    })
                return {'encontrado': True, 'afiliados': afiliados}
            else:
                # Modo validación: retornar un solo resultado
                fila = resultados_filtro.iloc[0]
                afiliado_base = str(fila['AFILIADO']).strip()
                cussp_base = str(fila['CUSSP']).strip()
                
                resultado = {
                    'encontrado': True,
                    'origen': 'REDIRECCIONAMIENTO',
                    'afiliado_base': afiliado_base,
                    'cussp': cussp_base,
                    'similitud': 0,
                    'observacion': ''
                }
                
                # Calcular similitud
                similitud = calcular_similitud(afiliado_busca, afiliado_base)
                resultado['similitud'] = round(similitud, 2)
                
                # Crear observación si no coincide
                if similitud < 0.95:
                    resultado['observacion'] = f"⚠️ Nombre no coincide exactamente. Base: {afiliado_base} | PDF: {afiliado_busca} (Similitud: {similitud*100:.1f}%)"
                else:
                    resultado['observacion'] = '✅ Validado'
                
                return resultado
    
    # Buscar en PRESUNTA si no encontró en REDIRECCIONAMIENTO
    if 'PRESUNTA' in bases:
        df = bases['PRESUNTA']
        
        # Búsqueda rápida usando el índice
        try:
            resultados_filtro = df.loc[[clave_busca]] if clave_busca in df.index else df[df['_doc_per'] == clave_busca]
        except:
            resultados_filtro = df[df['_doc_per'] == clave_busca]
        
        # Si tenemos CUSSP, filtrar también por eso
        if cussp_busca and not resultados_filtro.empty:
            resultados_filtro = resultados_filtro[resultados_filtro['CUSSP'] == cussp_busca]
        
        if not resultados_filtro.empty:
            if es_fallback:
                # Modo fallback: retornar TODOS los afiliados encontrados
                afiliados = []
                for _, fila in resultados_filtro.iterrows():
                    afiliados.append({
                        'cussp': str(fila['CUSSP']).strip(),
                        'afiliado': str(fila['AFILIADO']).strip(),
                        'origen': 'PRESUNTA',
                        'observacion': f"Datos de base local (PRESUNTA)"
                    })
                return {'encontrado': True, 'afiliados': afiliados}
            else:
                # Modo validación: retornar un solo resultado
                fila = resultados_filtro.iloc[0]
                afiliado_base = str(fila['AFILIADO']).strip()
                cussp_base = str(fila['CUSSP']).strip()
                
                resultado = {
                    'encontrado': True,
                    'origen': 'PRESUNTA',
                    'afiliado_base': afiliado_base,
                    'cussp': cussp_base,
                    'similitud': 0,
                    'observacion': ''
                }
                
                similitud = calcular_similitud(afiliado_busca, afiliado_base)
                resultado['similitud'] = round(similitud, 2)
                
                if similitud < 0.95:
                    resultado['observacion'] = f"⚠️ Nombre no coincide exactamente. Base: {afiliado_base} | PDF: {afiliado_busca} (Similitud: {similitud*100:.1f}%)"
                else:
                    resultado['observacion'] = '✅ Validado'
                
                return resultado
    
    # Si no encontró en ninguna base
    if es_fallback:
        return {'encontrado': False, 'afiliados': []}
    else:
        return {
            'encontrado': False,
            'origen': None,
            'afiliado_base': None,
            'cussp': None,
            'similitud': 0,
            'observacion': "⚠️ No encontrado en bases locales"
        }
