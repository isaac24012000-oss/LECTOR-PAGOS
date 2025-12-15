#!/usr/bin/env python3
"""
Punto de entrada para la aplicación en Streamlit Cloud
"""
import sys
from pathlib import Path

# Asegurar que el módulo utils esté disponible
sys.path.insert(0, str(Path(__file__).parent))

# Importar la aplicación principal
from app_planillas import *

if __name__ == "__main__":
    pass
