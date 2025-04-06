"""
Módulo para la gestión de encabezados y pies de página en los PDFs de despliegues operativos.
"""

import os
import datetime
import locale
from reportlab.lib import colors
from reportlab.lib.units import cm
from config import PDF_HEADER, PDF_FOOTER
from pdf_config import IMAGES_DIR
from image_utils import cargar_imagen_svg

# Definir colores
COLOR_AZUL = colors.navy
COLOR_NEGRO = colors.black
COLOR_DORADO = colors.HexColor('#D4AF37')  # Color dorado para el título

# Intentar configurar el locale para fechas en español
try:
    locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')
except:
    try:
        locale.setlocale(locale.LC_TIME, 'es_ES')
    except:
        pass  # Si no se puede configurar, se usará el formato por defecto

def encabezado_pie_pagina(canvas, doc):
    """
    Función para crear encabezado y pie de página en el PDF.
    
    Args:
        canvas: Objeto canvas de ReportLab
        doc: Documento PDF
    """
    # Guardar estado
    canvas.saveState()
    
    # Obtener ancho y alto de la página
    page_width = canvas._pagesize[0]
    page_height = canvas._pagesize[1]
    
    # Definir posición vertical para todos los elementos del encabezado
    posicion_y_titulo = page_height - doc.topMargin + 1.2*cm
    posicion_y_subtitulo = page_height - doc.topMargin + 0.8*cm
    
    # Logo (a la izquierda) - Tamaño reducido
    logo_filename = 'logo-gr-dorado.svg'
    drawing = cargar_imagen_svg(logo_filename, ancho=1.8*cm, alto=1.8*cm)
    
    if drawing:
        # Posicionar en la esquina superior izquierda, alineado con el título
        x_pos = doc.leftMargin
        # Ajustar la posición vertical para que el centro del logo esté alineado con el título
        y_pos = posicion_y_titulo - 0.9*cm  # Centrar el logo (altura 1.8cm) con el texto
        
        # Dibujar el logo
        drawing.drawOn(canvas, x_pos, y_pos)
    
    # Fecha actual (a la derecha)
    now = datetime.datetime.now()
    
    # Formatear fecha en español (17 de marzo de 2025)
    try:
        fecha_text = now.strftime('%d de %B de %Y').lower()
        # Capitalizar primera letra
        fecha_text = fecha_text[0].upper() + fecha_text[1:]
    except:
        # Si falla el formato en español, usar formato alternativo
        fecha_text = now.strftime('%d/%m/%Y')
    
    # Formatear hora (19:30)
    hora_text = now.strftime('%H:%M')
    
    # Calcular ancho aproximado del texto para alinearlo a la derecha
    fecha_width = canvas.stringWidth(fecha_text, 'Helvetica', 9)
    hora_width = canvas.stringWidth(hora_text, 'Helvetica', 9)
    
    # Dibujar fecha (a la derecha) - Tamaño reducido
    canvas.setFont('Helvetica', 9)
    canvas.setFillColor(COLOR_NEGRO)
    canvas.drawString(
        page_width - doc.rightMargin - fecha_width, 
        posicion_y_titulo,
        fecha_text
    )
    
    # Dibujar hora (a la derecha) - Tamaño reducido
    canvas.setFont('Helvetica', 9)
    canvas.drawString(
        page_width - doc.rightMargin - hora_width, 
        posicion_y_subtitulo,
        hora_text
    )
    
    # Título principal (centrado) - Tamaño reducido
    canvas.setFont('Helvetica-Bold', 12)
    canvas.setFillColor(COLOR_DORADO)
    canvas.drawCentredString(
        page_width / 2, 
        posicion_y_titulo,
        "DIRECCIÓN NACIONAL GUARDIA REPUBLICANA"
    )
    
    # Subtítulo (centrado) - Tamaño reducido
    canvas.setFont('Helvetica', 10)
    canvas.drawCentredString(
        page_width / 2, 
        posicion_y_subtitulo,
        "Estado Mayor Policial"
    )
    
    # Línea horizontal debajo del encabezado
    canvas.setStrokeColor(COLOR_DORADO)
    canvas.setLineWidth(1)
    canvas.line(
        doc.leftMargin, 
        page_height - doc.topMargin + 0.2*cm, # Ajustado para reducir el espacio
        page_width - doc.rightMargin, 
        page_height - doc.topMargin + 0.2*cm  # Ajustado para reducir el espacio
    )
    
    # Pie de página
    footer_text = PDF_FOOTER % canvas.getPageNumber()
    canvas.setFont('Helvetica', 8)
    canvas.setFillColor(COLOR_NEGRO)
    canvas.drawCentredString(
        page_width / 2, 
        doc.bottomMargin - 0.8*cm, 
        footer_text
    )
    
    # Línea horizontal encima del pie de página
    canvas.setStrokeColor(COLOR_AZUL)
    canvas.line(
        doc.leftMargin, 
        doc.bottomMargin - 0.4*cm, 
        page_width - doc.rightMargin, 
        doc.bottomMargin - 0.4*cm
    )
    
    # Restaurar estado
    canvas.restoreState()
