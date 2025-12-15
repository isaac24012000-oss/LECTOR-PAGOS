# Configuración de Secretos para Streamlit Cloud

## Instrucciones para agregar las URLs de GitHub a Streamlit Cloud

### Paso 1: Subir archivos Excel a GitHub

1. Abre tu repositorio en GitHub
2. Navega a la carpeta `LECTOR-PAGOS/`
3. Sube estos archivos:
   - `DETALLE AFILIADOS REDIRECCIONAMIENTO.xlsx`
   - `DETALLE AFILIADOS PRESUNTA.xlsx`

### Paso 2: Obtener las URLs raw

1. En GitHub, navega a `LECTOR-PAGOS/DETALLE AFILIADOS REDIRECCIONAMIENTO.xlsx`
2. Haz clic en el botón **Raw** (arriba a la derecha)
3. Copia la URL completa de la barra de direcciones
4. Repite para `DETALLE AFILIADOS PRESUNTA.xlsx`

Las URLs deberán verse así:
```
https://raw.githubusercontent.com/TU_USUARIO/TU_REPO/main/LECTOR-PAGOS/DETALLE%20AFILIADOS%20REDIRECCIONAMIENTO.xlsx
https://raw.githubusercontent.com/TU_USUARIO/TU_REPO/main/LECTOR-PAGOS/DETALLE%20AFILIADOS%20PRESUNTA.xlsx
```

### Paso 3: Configurar en Streamlit Cloud

1. Ve a [https://share.streamlit.io](https://share.streamlit.io)
2. Abre tu aplicación "LECTOR-PAGOS"
3. Haz clic en los **⋮** (menú) → **Settings**
4. En la sección **Secrets**, pega lo siguiente:

```toml
GITHUB_REDI_URL = "https://raw.githubusercontent.com/TU_USUARIO/TU_REPO/main/LECTOR-PAGOS/DETALLE%20AFILIADOS%20REDIRECCIONAMIENTO.xlsx"
GITHUB_PRES_URL = "https://raw.githubusercontent.com/TU_USUARIO/TU_REPO/main/LECTOR-PAGOS/DETALLE%20AFILIADOS%20PRESUNTA.xlsx"
```

⚠️ **Importante**: Reemplaza:
- `TU_USUARIO` con tu usuario de GitHub
- `TU_REPO` con el nombre de tu repositorio
- Mantén `main` si es tu rama principal (o `master` si usas esa)

5. Haz clic en **Save**
6. La app se reiniciará automáticamente

### Paso 4: Verificar que funciona

Una vez configurado, deberías ver en la terminal:
```
📥 Intentando cargar REDIRECCIONAMIENTO desde GitHub...
✅ REDIRECCIONAMIENTO cargado desde GitHub
📥 Intentando cargar PRESUNTA desde GitHub...
✅ PRESUNTA cargado desde GitHub
```

## Alternativa: Usar .streamlit/secrets.toml localmente

Si quieres probar localmente sin subir a Streamlit Cloud aún:

1. Crea la carpeta `.streamlit` en la raíz del proyecto (si no existe)
2. Crea un archivo `secrets.toml` dentro
3. Pega:

```toml
GITHUB_REDI_URL = "https://raw.githubusercontent.com/TU_USUARIO/TU_REPO/main/LECTOR-PAGOS/DETALLE%20AFILIADOS%20REDIRECCIONAMIENTO.xlsx"
GITHUB_PRES_URL = "https://raw.githubusercontent.com/TU_USUARIO/TU_REPO/main/LECTOR-PAGOS/DETALLE%20AFILIADOS%20PRESUNTA.xlsx"
```

4. Reinicia Streamlit con: `streamlit run app_planillas.py`

⚠️ **IMPORTANTE**: No subas `.streamlit/secrets.toml` a GitHub. Ya está en `.gitignore` (debería estarlo).

## Troubleshooting

**Problema**: "Error descargando desde GitHub"
- ✅ Verifica que las URLs sean correctas
- ✅ Verifica que los archivos Excel estén públicos en GitHub
- ✅ Intenta abrir la URL en el navegador

**Problema**: Aún usa rutas locales
- ✅ Verifica que las variables de entorno se hayan guardado en Streamlit Cloud
- ✅ Espera 1-2 minutos para que Streamlit Cloud actualice
- ✅ Reinicia la app manualmente desde el menú

**Problema**: "KeyError GITHUB_REDI_URL"
- ✅ Asegúrate de que los secretos se guardaron correctamente
- ✅ Reinicia la aplicación en Streamlit Cloud
