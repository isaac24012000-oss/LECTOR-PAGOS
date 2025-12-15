# Lector de Planillas de Pago

Aplicación web para extraer y procesar datos de archivos PDF de planillas de pago de forma automática.

## 🚀 Características

- ✅ Extracción automática de datos de PDFs de planillas
- ✅ Procesa múltiples archivos simultáneamente
- ✅ Exporta datos a Excel con formato profesional
- ✅ Interfaz amigable con Streamlit
- ✅ Título personalizado: "PLANTILLA PAGOS REDIRECCIONAMIENTO"
- ✅ Incluye razón social del empleador

## 📋 Campos Extraídos

- **RUC**: Número de RUC del empleador
- **RAZON_SOCIAL**: Nombre de la empresa
- **PERIODO**: Período de devengue (sin guiones)
- **CUSSP**: Código único de seguro de pensiones del afiliado
- **AFILIADO**: Nombre del trabajador afiliado
- **FECHA_PAGO**: Fecha de pago de la planilla
- **N_PLANILLA**: Número de la planilla
- **MONTO**: Total de aporte (Fondo Pensiones + Retenciones)

## 🔧 Instalación Local

### Requisitos
- Python 3.8 o superior
- pip (gestor de paquetes)

### Pasos

1. Clonar el repositorio:
```bash
git clone <tu-repo-url>
cd "LECTOR DE PAGOS"
```

2. Crear un entorno virtual (opcional pero recomendado):
```bash
python -m venv venv
venv\Scripts\activate
```

3. Instalar dependencias:
```bash
pip install -r requirements.txt
```

4. Ejecutar la aplicación:
```bash
streamlit run app_planillas.py
```

5. La aplicación se abrirá en tu navegador en `http://localhost:8501`

## ☁️ Desplegar en Streamlit Cloud

### Opción 1: Desplegar automáticamente

1. Sube tu código a GitHub
2. Ve a [Streamlit Cloud](https://streamlit.io/cloud)
3. Conecta tu cuenta de GitHub
4. Selecciona el repositorio y rama
5. Selecciona `app_planillas.py` como archivo principal
6. ¡Listo! Tu app estará disponible en línea

### Opción 2: Desplegar manualmente

1. Crea una cuenta en [Streamlit Cloud](https://streamlit.io/cloud)
2. Conecta tu repositorio de GitHub
3. Streamlit Cloud detectará automáticamente `app_planillas.py`

## 📦 Estructura de Carpetas

```
LECTOR DE PAGOS/
├── app_planillas.py          # Aplicación principal
├── requirements.txt           # Dependencias de Python
├── README.md                  # Este archivo
├── .streamlit/
│   └── config.toml            # Configuración de Streamlit
├── .gitignore                 # Archivos a ignorar en Git
└── utils/
    ├── __init__.py
    ├── excel_generator.py     # Generador de Excel
    ├── file_processor.py      # Procesador de archivos
    └── google_ocr.py          # Funciones OCR
```

## 🔐 Seguridad

- Los archivos PDF se procesan localmente
- No se guardan datos en servidores externos
- Cada sesión es independiente

## 📞 Soporte

Para reportar errores o sugerencias, contacta al desarrollador.

## 📄 Licencia

Este proyecto es de uso privado.

---

**Última actualización**: 15 de diciembre de 2025
