"""
Utilidades para la generación de reportes de cumplimiento.
"""

from datetime import datetime
from reportlab.platypus import Paragraph, Spacer, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.units import cm
from reportlab.lib.styles import getSampleStyleSheet

def obtener_estilos_parrafo():
    """
    Obtiene los estilos para párrafos utilizados en los reportes.
    
    Returns:
        dict: Diccionario con los estilos para párrafos.
    """
    styles = getSampleStyleSheet()
    
    title_style = styles['Heading1']
    title_style.alignment = 1  # Centrado
    title_style.textColor = colors.Color(0.8, 0.6, 0.0)  # Color dorado
    
    subtitle_style = styles['Heading2']
    subtitle_style.alignment = 1  # Centrado
    
    normal_style = styles['Normal']
    
    return {
        'title': title_style,
        'subtitle': subtitle_style,
        'normal': normal_style
    }

def obtener_fecha_actual_formateada():
    """
    Obtiene la fecha actual formateada en español.
    
    Returns:
        str: Fecha actual formateada.
    """
    return datetime.now().strftime("%d de %B de %Y").replace("January", "Enero").replace("February", "Febrero").replace("March", "Marzo").replace("April", "Abril").replace("May", "Mayo").replace("June", "Junio").replace("July", "Julio").replace("August", "Agosto").replace("September", "Septiembre").replace("October", "Octubre").replace("November", "Noviembre").replace("December", "Diciembre")

def obtener_mes_actual_formateado():
    """
    Obtiene el mes actual formateado en español.
    
    Returns:
        str: Mes actual formateado.
    """
    return datetime.now().strftime("%B").replace("January", "Enero").replace("February", "Febrero").replace("March", "Marzo").replace("April", "Abril").replace("May", "Mayo").replace("June", "Junio").replace("July", "Julio").replace("August", "Agosto").replace("September", "Septiembre").replace("October", "Octubre").replace("November", "Noviembre").replace("December", "Diciembre")

def crear_tabla_con_estilo(datos, encabezados, colWidths=None):
    """
    Crea una tabla con estilo para los reportes.
    
    Args:
        datos (list): Lista de datos para la tabla.
        encabezados (list): Lista de encabezados para la tabla.
        colWidths (list, optional): Lista de anchos para las columnas.
            Defaults to None.
            
    Returns:
        Table: Tabla con estilo.
    """
    # Añadir encabezados a los datos
    datos_completos = [encabezados] + datos
    
    # Crear tabla
    tabla = Table(datos_completos, colWidths=colWidths)
    
    # Aplicar estilo a la tabla
    tabla.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.Color(0.8, 0.6, 0.0)),  # Color dorado para encabezado
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 5),
        ('BACKGROUND', (0, 1), (-1, -2), colors.white),
        ('BACKGROUND', (0, -1), (-1, -1), colors.lightgrey),  # Fila de totales
        ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),  # Negrita para totales
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('ALIGN', (1, 1), (-1, -1), 'CENTER'),
    ]))
    
    return tabla
