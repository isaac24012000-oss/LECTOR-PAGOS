# Configuración para Streamlit Cloud

## Opción 1: Variables de Entorno (Recomendado)

Para que Streamlit Cloud descargue automáticamente los archivos Excel desde GitHub, debes configurar variables de entorno en tu aplicación Streamlit Cloud.

### Pasos:

1. Ve a tu aplicación en [Streamlit Cloud](https://share.streamlit.io)
2. Abre la aplicación y haz clic en el menú (⋯) en la esquina superior derecha
3. Selecciona "Settings"
4. En la sección "Secrets", agrega estas variables:

```
GITHUB_REDI_URL=https://raw.githubusercontent.com/TU_USUARIO/TU_REPO/main/LECTOR-PAGOS/DETALLE%20AFILIADOS%20REDIRECCIONAMIENTO.xlsx
GITHUB_PRES_URL=https://raw.githubusercontent.com/TU_USUARIO/TU_REPO/main/LECTOR-PAGOS/DETALLE%20AFILIADOS%20PRESUNTA.xlsx
```

### Cómo obtener las URLs correctas:

1. Ve a tu repositorio en GitHub
2. Navega a la carpeta `LECTOR-PAGOS`
3. Haz clic en el archivo Excel
4. Haz clic en el botón "Raw" (crudo)
5. Copia la URL completa de la barra de direcciones

**Ejemplo de URL correcta:**
```
https://raw.githubusercontent.com/usuario/lector-pagos/main/LECTOR-PAGOS/DETALLE%20AFILIADOS%20REDIRECCIONAMIENTO.xlsx
```

Reemplaza:
- `usuario` con tu nombre de usuario de GitHub
- `lector-pagos` con el nombre de tu repositorio
- `main` con la rama que uses (puede ser `main`, `master`, etc.)

## Opción 2: Modificar directamente el código

Si no quieres usar variables de entorno, edita el archivo `utils/validador_base_local.py`:

Busca estas líneas (alrededor de la línea 105):

```python
github_url_redi = os.environ.get(
    'GITHUB_REDI_URL',
    'https://raw.githubusercontent.com/TU_USUARIO/TU_REPO/main/LECTOR-PAGOS/DETALLE%20AFILIADOS%20REDIRECCIONAMIENTO.xlsx'
)
```

Y reemplaza los URLs por los correctos.

## Testeo local

Para testear que funcione localmente:
1. Asegúrate de que los archivos Excel estén en la carpeta `LECTOR-PAGOS/`
2. Ejecuta `streamlit run app_planillas.py`
3. Deberías ver un mensaje ✅ indicando de dónde se cargaron

## Notas importantes

- Los archivos Excel deben estar en la rama principal que uses
- Las URLs deben tener `%20` en lugar de espacios en blanco
- Streamlit Cloud solo puede acceder a repositorios públicos o a las que tengas permisos
