#!/bin/bash
# Script para configurar Git y hacer push a GitHub
# Úsalo si estás en WSL o Git Bash en Windows

# Configurar Git (primera vez)
git config --global user.name "Tu Nombre"
git config --global user.email "tu.email@example.com"

# Inicializar repositorio
git init

# Agregar todos los archivos
git add .

# Hacer commit
git commit -m "Inicial: Lector de Planillas - Versión 1.0"

# Cambiar rama a main (si no lo está ya)
git branch -M main

# Agregar remoto (reemplazar con tu URL de GitHub)
git remote add origin https://github.com/tu-usuario/lector-planillas.git

# Hacer push
git push -u origin main

echo "✅ Repositorio configurado y subido a GitHub"
echo "📌 Ahora ve a https://streamlit.io/cloud y haz clic en 'New app'"
