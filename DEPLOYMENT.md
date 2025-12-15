# Instrucciones de Deployment

## 📌 Pasos para desplegar en Streamlit Cloud

### 1. Preparar el repositorio en GitHub

```bash
# Inicializar Git
git init

# Agregar todos los archivos
git add .

# Hacer commit
git commit -m "Inicial: Lector de Planillas"

# Agregar remoto (cambiar URL con tu repositorio)
git remote add origin https://github.com/tu-usuario/lector-planillas.git

# Hacer push
git push -u origin main
```

### 2. Configurar en Streamlit Cloud

1. Ve a https://streamlit.io/cloud
2. Haz clic en "New app"
3. Selecciona:
   - **Repository**: tu-usuario/lector-planillas
   - **Branch**: main
   - **Main file path**: app_planillas.py
4. Haz clic en "Deploy"

### 3. Esperar a que se despliegue

- Streamlit Cloud instalará las dependencias de `requirements.txt`
- La aplicación estará disponible en: `https://[nombre-app].streamlit.app`

## ✅ Verificación

Después de desplegar, verifica que:
- [ ] La aplicación cargue sin errores
- [ ] Puedas cargar archivos PDF
- [ ] Se extraigan los datos correctamente
- [ ] La exportación a Excel funcione

## 🔧 Configuraciones recomendadas

En Streamlit Cloud (Settings > Secrets), puedes agregar:

```toml
# .streamlit/secrets.toml
[logger]
level = "info"
```

## 📝 Notas

- Los archivos PDF se procesan temporalmente en la sesión
- No se guardan permanentemente en el servidor
- Cada usuario tiene su propia sesión independiente
- Máximo de carga: 200 MB

## 🆘 Troubleshooting

### La app no se despliega
- Verifica que `app_planillas.py` existe en la raíz
- Revisa los logs en Streamlit Cloud

### Error "ModuleNotFoundError"
- Verifica que todas las librerías estén en `requirements.txt`
- Revisa la ortografía exacta de los nombres

### Carga lenta
- Los archivos grandes pueden tardarse en procesar
- Streamlit Cloud tiene limitaciones de recursos

## 📞 Soporte

Para más información: https://docs.streamlit.io/streamlit-cloud
