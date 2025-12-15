@echo off
REM Script para configurar Git y hacer push a GitHub en Windows

REM Configurar Git (primera vez)
git config --global user.name "Tu Nombre"
git config --global user.email "tu.email@example.com"

REM Inicializar repositorio
git init

REM Agregar todos los archivos
git add .

REM Hacer commit
git commit -m "Inicial: Lector de Planillas - Version 1.0"

REM Cambiar rama a main
git branch -M main

REM Agregar remoto (reemplazar con tu URL de GitHub)
git remote add origin https://github.com/tu-usuario/lector-planillas.git

REM Hacer push
git push -u origin main

echo.
echo ===================================
echo Repositorio configurado exitosamente
echo ===================================
echo.
echo SIGUIENTES PASOS:
echo 1. Ve a https://streamlit.io/cloud
echo 2. Conecta con tu cuenta de GitHub
echo 3. Haz clic en "New app"
echo 4. Selecciona tu repositorio
echo 5. Cambia Main file path a: app_planillas.py
echo 6. Haz clic en Deploy
echo.
pause
