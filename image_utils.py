"""
Utilidades para el manejo de imágenes en la generación de PDFs.
"""

import os
from reportlab.graphics.shapes import Drawing, Group, translate, Rect
from reportlab.platypus import Image
from reportlab.graphics.renderPDF import draw
from svglib.svglib import svg2rlg
from pdf_config import IMAGES_DIR, IMAGEN_ANCHO, IMAGEN_ALTO

def cargar_imagen_svg(nombre_archivo, ancho=IMAGEN_ANCHO, alto=IMAGEN_ALTO):
    """
    Carga una imagen SVG y la convierte en un objeto Drawing de ReportLab.
    
    Args:
        nombre_archivo: Nombre del archivo SVG
        ancho: Ancho deseado de la imagen
        alto: Alto deseado de la imagen
        
    Returns:
        Drawing: Objeto Drawing de ReportLab o None si no se pudo cargar
    """
    ruta_completa = os.path.join(IMAGES_DIR, nombre_archivo)
    print(f"Intentando cargar imagen: {ruta_completa}")
    
    # Verificar si es un archivo SVG
    if nombre_archivo.lower().endswith('.svg') and os.path.exists(ruta_completa):
        try:
            # Convertir SVG a un objeto Drawing de ReportLab
            drawing = svg2rlg(ruta_completa)
            if drawing:
                print(f"  ✓ Imagen SVG cargada correctamente: {nombre_archivo}")
                
                # Ajustar tamaño
                ratio = min(ancho/drawing.width, alto/drawing.height) if drawing.width and drawing.height else 1
                drawing.width, drawing.height = drawing.width*ratio, drawing.height*ratio
                drawing.scale(ratio, ratio)
                
                # Centrar en el espacio disponible
                x_offset = (ancho - drawing.width) / 2
                y_offset = (alto - drawing.height) / 2
                
                # Crear un nuevo Drawing con el tamaño deseado
                new_drawing = Drawing(ancho, alto)
                drawing.translate(x_offset, y_offset)
                new_drawing.add(drawing)
                
                return new_drawing
            else:
                print(f"  ✗ Error: El SVG se cargó pero el objeto drawing es None: {nombre_archivo}")
        except Exception as e:
            print(f"  ✗ Error al cargar la imagen SVG {nombre_archivo}: {e}")
    
    # Para archivos que no son SVG o si falla la carga del SVG
    if os.path.exists(ruta_completa) and not nombre_archivo.lower().endswith('.svg'):
        try:
            img = Image(ruta_completa, width=ancho, height=alto)
            return img
        except Exception as e:
            print(f"  ✗ Error al cargar la imagen {nombre_archivo}: {e}")
    
    # Si no se encuentra la imagen original, buscar alternativas
    nombre_base = os.path.splitext(nombre_archivo)[0]
    for ext in ['.png', '.jpg', '.jpeg']:
        alt_path = os.path.join(IMAGES_DIR, nombre_base + ext)
        if os.path.exists(alt_path):
            try:
                img = Image(alt_path, width=ancho, height=alto)
                return img
            except Exception as e:
                print(f"Error al cargar imagen alternativa {alt_path}: {e}")
    
    # Si no hay imagen, devolver None
    return None

def usar_imagen_rasterizada(nombre_archivo, ancho=IMAGEN_ANCHO, alto=IMAGEN_ALTO):
    """
    Alternativa para usar imágenes rasterizadas (PNG, JPG) en lugar de SVG.
    
    Args:
        nombre_archivo: Nombre del archivo SVG (se intentará buscar PNG/JPG con mismo nombre)
        ancho: Ancho deseado de la imagen
        alto: Alto deseado de la imagen
        
    Returns:
        Image: Objeto Image de ReportLab o None si no se pudo cargar
    """
    # Extraer nombre base sin extensión
    nombre_base = os.path.splitext(nombre_archivo)[0]
    
    # Probar con diferentes extensiones
    for ext in ['.png', '.jpg', '.jpeg']:
        ruta_completa = os.path.join(IMAGES_DIR, nombre_base + ext)
        if os.path.exists(ruta_completa):
            try:
                img = Image(ruta_completa, width=ancho, height=alto)
                return img
            except Exception as e:
                print(f"Error al cargar imagen alternativa {ruta_completa}: {e}")
    
    return None
