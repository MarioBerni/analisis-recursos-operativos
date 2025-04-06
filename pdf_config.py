"""
Configuraciones para la generación de PDFs de despliegues operativos.
"""

import os
from reportlab.lib.units import cm

# Ruta a la carpeta de imágenes
IMAGES_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'images')

# Columnas a mostrar en el PDF
COLUMNAS_PDF = [
    "NOMBRE ORDEN",
    "MOVILES",
    "SS.OO",
    "MOTOS",
    "HIPO",
    "PP.SS PIE TIERRA",
    "CHOQUE APOSTADO",
    "PP.SS TOTAL",
    "HORA INICIO",
    "HORA FIN",
    "SECC."
]

# Cabeceras personalizadas para las columnas (para columnas sin imagen)
CABECERAS_PERSONALIZADAS = {
    "UNIDAD": "UNIDAD",
    "NOMBRE ORDEN": "NOMBRE ORDEN",
    "HORA INICIO": "HORA\nINICIO",
    "HORA FIN": "HORA\nFIN",
    "SECC.": "SECC."
}

# Mapeo de columnas a imágenes SVG
COLUMNAS_IMAGENES = {
    "MOVILES": "movil.svg",
    "SS.OO": "ssoo.svg",
    "MOTOS": "motos.svg",
    "HIPO": "hipos.svg",
    "PP.SS PIE TIERRA": "pieTierra.svg",
    "CHOQUE APOSTADO": "choqueApostado.svg",
    "PP.SS TOTAL": "ppssTotal.svg"
}

# Tamaño estándar para todas las imágenes de cabecera
IMAGEN_ANCHO = 0.9*cm
IMAGEN_ALTO = 0.9*cm

# Anchos de columna para la tabla del PDF
ANCHOS_COLUMNAS = [
    5.5*cm,   # NOMBRE ORDEN
    1.5*cm,   # MOVILES
    1.5*cm,   # SS.OO
    1.5*cm,   # MOTOS
    1.5*cm,   # HIPO
    1.5*cm,   # PP.SS PIE TIERRA
    1.5*cm,   # CHOQUE APOSTADO
    1.5*cm,   # PP.SS TOTAL
    1.8*cm,   # HORA INICIO
    1.8*cm,   # HORA FIN
    2.0*cm,   # SECC.
]

# Verificar la existencia de los archivos SVG al cargar el módulo
def verificar_imagenes():
    """Verifica si existen los archivos de imagen configurados."""
    for col, svg_file in COLUMNAS_IMAGENES.items():
        ruta_completa = os.path.join(IMAGES_DIR, svg_file)
        if os.path.exists(ruta_completa):
            print(f"✓ Archivo SVG encontrado: {svg_file}")
        else:
            print(f"✗ Archivo SVG NO encontrado: {svg_file}")
