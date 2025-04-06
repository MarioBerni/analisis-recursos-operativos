"""
Utilidades para la creación y aplicación de estilos en tablas de PDFs.
"""

from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

def crear_estilos_tabla():
    """
    Crea un diccionario con los estilos para la tabla.
    
    Returns:
        dict: Diccionario con los estilos para la tabla.
    """
    # Obtener estilos base
    estilos_base = getSampleStyleSheet()
    
    # Crear estilos personalizados
    estilo_primera_columna = ParagraphStyle(
        'PrimeraColumna',
        parent=estilos_base['Normal'],
        fontName='Helvetica',  # Quitamos la negrita (Helvetica-Bold -> Helvetica)
        fontSize=9,
        leading=10,
        alignment=0,  # 0 = izquierda
        spaceAfter=0,
        spaceBefore=0
    )
    
    estilo_datos = ParagraphStyle(
        'Datos',
        parent=estilos_base['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=10,
        alignment=1,  # 1 = centro
        spaceAfter=0,
        spaceBefore=0
    )
    
    # Definir colores para la tabla
    color_encabezado_fondo = colors.navy
    color_encabezado_texto = colors.white
    
    # Crear diccionario de estilos
    estilos = {
        'first_col': estilo_primera_columna,
        'data': estilo_datos,
        'header_bg': color_encabezado_fondo,
        'header_fg': color_encabezado_texto
    }
    
    return estilos

def crear_estilo_tabla_detallado(columnas_con_imagenes, estilos):
    """
    Crea un estilo detallado para las tablas del PDF.
    
    Args:
        columnas_con_imagenes (list): Lista de índices de columnas que contienen imágenes.
        estilos (dict): Diccionario con los estilos para la tabla.
        
    Returns:
        list: Lista de tuplas con los estilos para la tabla.
    """
    # Crear estilo base para la tabla
    estilo_tabla = [
        # Estilo para todas las celdas
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('ALIGN', (0, 0), (-1, 0), 'CENTER'),  # Centrar encabezados
        ('ALIGN', (0, 1), (0, -1), 'LEFT'),    # Alinear a la izquierda la primera columna
        ('ALIGN', (1, 1), (-1, -1), 'CENTER'),  # Centrar el resto de datos
        
        # Estilo para el encabezado
        ('BACKGROUND', (0, 0), (-1, 0), estilos['header_bg']),
        ('TEXTCOLOR', (0, 0), (-1, 0), estilos['header_fg']),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        
        # Líneas de la tabla
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('BOX', (0, 0), (-1, -1), 1, colors.black),
        ('LINEABOVE', (0, 1), (-1, 1), 1, colors.black),  # Línea gruesa después del encabezado
        
        # Espaciado de celdas
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
        ('LEFTPADDING', (0, 0), (-1, -1), 3),
        ('RIGHTPADDING', (0, 0), (-1, -1), 3),
        
        # Espaciado adicional para el encabezado (reducido)
        ('TOPPADDING', (0, 0), (-1, 0), 4),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 4),
    ]
    
    # Aplicar estilos especiales para columnas con imágenes
    for i in columnas_con_imagenes:
        # Alineación centrada para las imágenes
        estilo_tabla.append(('ALIGN', (i, 0), (i, 0), 'CENTER'))
        estilo_tabla.append(('VALIGN', (i, 0), (i, 0), 'MIDDLE'))
        # Fondo blanco para las celdas con imágenes para mejor visualización
        estilo_tabla.append(('BACKGROUND', (i, 0), (i, 0), colors.white))
        # Padding ajustado para las imágenes
        estilo_tabla.append(('TOPPADDING', (i, 0), (i, 0), 5))
        estilo_tabla.append(('BOTTOMPADDING', (i, 0), (i, 0), 5))
    
    return estilo_tabla

def aplicar_colores_alternos(estilo_tabla, filas_total):
    """
    Aplica colores alternos a las filas de la tabla para mejorar la legibilidad.
    
    Args:
        estilo_tabla (list): Lista de tuplas con los estilos para la tabla.
        filas_total (int): Número total de filas en la tabla.
        
    Returns:
        list: Lista de tuplas con los estilos para la tabla, incluyendo colores alternos.
    """
    # Color para filas alternas
    color_alterno = colors.lightgrey
    
    # Aplicar color alterno a filas pares (comenzando desde la fila 1, que es la primera fila de datos)
    # La fila 0 es el encabezado, las filas de datos comienzan en el índice 1
    for i in range(0, filas_total, 2):
        # Sumar 1 al índice i para saltar el encabezado (fila 0)
        estilo_tabla.append(('BACKGROUND', (0, i+1), (-1, i+1), color_alterno))
    
    return estilo_tabla
