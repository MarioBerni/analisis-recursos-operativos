"""
Estilos y formatos para la generación de PDFs de despliegues operativos.
"""

import datetime
import os
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.units import cm
from reportlab.platypus import Paragraph, TableStyle
from config import PDF_HEADER, PDF_FOOTER
from pdf_config import IMAGES_DIR

def crear_estilos():
    """
    Crea y devuelve los estilos para el documento PDF.
    
    Returns:
        dict: Diccionario con los estilos para el documento
    """
    # Obtener estilos base
    styles = getSampleStyleSheet()
    
    # Crear estilo personalizado para el título
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=18,
        textColor=colors.navy,
        alignment=TA_CENTER,
        spaceAfter=0.5*cm
    )
    
    # Crear estilo para subtítulos
    subtitle_style = ParagraphStyle(
        'Subtitle',
        parent=styles['Normal'],
        fontSize=10,
        textColor=colors.darkslategray,
        alignment=TA_CENTER,
        spaceAfter=1*cm
    )
    
    # Crear estilo para cabeceras de tabla
    header_style = ParagraphStyle(
        'Header',
        parent=styles['Normal'],
        fontSize=9,
        textColor=colors.white,
        alignment=TA_CENTER,
        leading=10
    )
    
    return {
        'title': title_style,
        'subtitle': subtitle_style,
        'Header': header_style,
        'Normal': styles['Normal'],
        'base': styles
    }

def crear_estilo_tabla():
    """
    Crea y devuelve el estilo para la tabla del PDF.
    
    Returns:
        TableStyle: Estilo para la tabla
    """
    return TableStyle([
        # Encabezados
        ('BACKGROUND', (0, 0), (-1, 0), colors.navy),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
        ('VALIGN', (0, 0), (-1, 0), 'MIDDLE'),  # Alineación vertical centrada para cabeceras
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 9),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 18),  # Aumentar el padding para dar más espacio a las imágenes
        ('TOPPADDING', (0, 0), (-1, 0), 18),     # Aumentar el padding para dar más espacio a las imágenes
        ('LEFTPADDING', (0, 0), (-1, 0), 6),     # Padding horizontal para centrar mejor
        ('RIGHTPADDING', (0, 0), (-1, 0), 6),    # Padding horizontal para centrar mejor
        
        # Datos
        ('BACKGROUND', (0, 1), (-1, -1), colors.white),
        ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
        ('ALIGN', (0, 1), (0, -1), 'LEFT'),  # Alineación izquierda para NOMBRE ORDEN
        ('ALIGN', (1, 1), (-1, -1), 'CENTER'),  # Alineación central para el resto
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 1), (-1, -1), 5),
        ('TOPPADDING', (0, 1), (-1, -1), 5),
        
        # Bordes y líneas
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('BOX', (0, 0), (-1, -1), 1, colors.black),
        ('LINEBELOW', (0, 0), (-1, 0), 1, colors.black),
        
        # Filas alternas para mejor legibilidad
        ('BACKGROUND', (0, 1), (-1, -1), colors.white),
    ])

def aplicar_colores_alternos(table_style, num_filas):
    """
    Aplica colores alternos a las filas de la tabla para mejor legibilidad.
    
    Args:
        table_style: Estilo de tabla al que aplicar los colores alternos
        num_filas: Número de filas en la tabla
        
    Returns:
        TableStyle: Estilo de tabla actualizado
    """
    for i in range(1, num_filas):
        if i % 2 == 0:
            table_style.add('BACKGROUND', (0, i), (-1, i), colors.lightgrey)
    return table_style

def header_footer(canvas, doc):
    """
    Función para crear encabezado y pie de página en el PDF.
    
    Args:
        canvas: Objeto canvas de ReportLab
        doc: Documento PDF
    """
    # Guardar estado
    canvas.saveState()
    
    # Logo (si existe)
    logo_path = os.path.join(IMAGES_DIR, 'logo.png')
    if os.path.exists(logo_path):
        # Ajustar tamaño y posición según necesidades
        canvas.drawImage(logo_path, doc.leftMargin, doc.height + doc.topMargin - 2*cm, width=2*cm, height=2*cm, preserveAspectRatio=True)
    
    # Encabezado
    canvas.setFont('Helvetica-Bold', 10)
    canvas.drawCentredString(doc.width/2.0 + doc.leftMargin, doc.height + doc.topMargin - 0.5*cm, PDF_HEADER)
    
    # Fecha actual
    now = datetime.datetime.now()
    date_text = f"Fecha de generación: {now.strftime('%d/%m/%Y %H:%M')}"
    canvas.setFont('Helvetica', 8)
    canvas.drawRightString(doc.width + doc.leftMargin - 1*cm, doc.height + doc.topMargin - 1*cm, date_text)
    
    # Línea horizontal debajo del encabezado
    canvas.setStrokeColor(colors.navy)
    canvas.setLineWidth(1)
    canvas.line(doc.leftMargin, doc.height + doc.topMargin - 1.2*cm, 
                doc.width + doc.leftMargin, doc.height + doc.topMargin - 1.2*cm)
    
    # Pie de página
    footer_text = PDF_FOOTER % doc.page
    canvas.setFont('Helvetica', 8)
    canvas.drawCentredString(doc.width/2.0 + doc.leftMargin, doc.bottomMargin - 0.5*cm, footer_text)
    
    # Línea horizontal encima del pie de página
    canvas.line(doc.leftMargin, doc.bottomMargin, 
                doc.width + doc.leftMargin, doc.bottomMargin)
    
    # Restaurar estado
    canvas.restoreState()
