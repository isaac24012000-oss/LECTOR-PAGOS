"""
Setup para la aplicación Lector de Planillas
"""
from setuptools import setup, find_packages

setup(
    name="lector-planillas",
    version="1.0.0",
    description="Aplicación para extraer datos de PDFs de planillas de pago",
    author="Tu Nombre",
    author_email="tu.email@example.com",
    packages=find_packages(),
    install_requires=[
        "streamlit>=1.28.0",
        "pandas>=2.0.0",
        "openpyxl>=3.1.0",
        "pillow>=9.5.0",
        "PyPDF2>=3.0.0",
        "pdfplumber>=0.10.0",
        "python-docx>=0.8.11",
    ],
    python_requires=">=3.8",
    entry_points={
        "console_scripts": [
            "lector-planillas=app_planillas:main",
        ],
    },
)
