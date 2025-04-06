"""
Módulo para la gestión de tablas en los PDFs de despliegues operativos.
"""

import pandas as pd
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.platypus import Table, TableStyle, Paragraph
from reportlab.lib.units import cm

# Definir colores
COLOR_AZUL = colors.navy
COLOR_GRIS_CLARO = colors.lightgrey
COLOR_BLANCO = colors.white
COLOR_NEGRO = colors.black

# Mapeo de nombres de columnas a nombres más cortos para el PDF
NOMBRES_COLUMNAS = {
    "UNIDAD": "UNIDAD",
    "NOMBRE ORDEN": "NOMBRE ORDEN",
    "MOVILES": "MÓVILES",
    "SS.OO": "SS.OO",
    "MOTOS": "MOTOS",
    "HIPO": "HIPO",
    "PP.SS PIE TIERRA": "PIE TIERRA",
    "CHOQUE APOSTADO": "CH. APOSTADO",
    "CHOQUE ALERTA": "CH. ALERTA",
    "PP.SS TOTAL": "TOTAL",
    "HORA INICIO": "INICIO",
    "HORA FIN": "FIN",
    "SECC.": "SECC."
}

# Mapeo de columnas a imágenes
ICONOS_COLUMNAS = {
    "MOVILES": "movil.svg",
    "SS.OO": "ssoo.svg",
    "MOTOS": "motos.svg",
    "HIPO": "hipos.svg",
    "PP.SS PIE TIERRA": "pieTierra.svg",
    "CHOQUE APOSTADO": "choqueApostado.svg",
    "CHOQUE ALERTA": "choqueEnAlerta.svg",
    "PP.SS TOTAL": "ppssTotal.svg"
}

def crear_estilos_tabla():
    """
    Crea los estilos de texto para la tabla del PDF.
    
    Returns:
        dict: Diccionario con los estilos para la tabla
    """
    # Estilo para cabeceras de tabla
    header_style = ParagraphStyle(
        'TableHeader',
        fontSize=8,
        textColor=COLOR_BLANCO,
        alignment=TA_CENTER,
        leading=10
    )
    
    # Estilo para datos de tabla
    data_style = ParagraphStyle(
        'TableData',
        fontSize=8,
        textColor=COLOR_NEGRO,
        alignment=TA_CENTER,
        leading=10
    )
    
    # Estilo para la primera columna (alineada a la izquierda)
    first_col_style = ParagraphStyle(
        'FirstColumn',
        fontSize=8,
        textColor=COLOR_NEGRO,
        alignment=TA_LEFT,
        leading=10
    )
    
    return {
        'header': header_style,
        'data': data_style,
        'first_col': first_col_style
    }

def crear_estilo_tabla(columnas_con_imagenes):
    """
    Crea el estilo base para la tabla del PDF.
    
    Args:
        columnas_con_imagenes: Lista de índices de columnas que contienen imágenes
        
    Returns:
        TableStyle: Estilo para la tabla
    """
    estilo_tabla = TableStyle([
        # Encabezados - Fondo azul para todas las cabeceras excepto las que tienen imágenes
        ('BACKGROUND', (0, 0), (-1, 0), COLOR_AZUL),
        ('TEXTCOLOR', (0, 0), (-1, 0), COLOR_BLANCO),
        ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 8),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
        ('TOPPADDING', (0, 0), (-1, 0), 8),
        
        # Datos
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 1), (-1, -1), 4),
        ('TOPPADDING', (0, 1), (-1, -1), 4),
        
        # Bordes y líneas
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('BOX', (0, 0), (-1, -1), 1, colors.black),
        ('LINEBELOW', (0, 0), (-1, 0), 1, colors.black),
    ])
    
    # Quitar el fondo azul de las columnas con imágenes y ajustar padding para celdas cuadradas
    for i in columnas_con_imagenes:
        estilo_tabla.add('BACKGROUND', (i, 0), (i, 0), COLOR_BLANCO)
        # Ajustar padding para hacer las celdas cuadradas
        estilo_tabla.add('LEFTPADDING', (i, 0), (i, 0), 0.15*cm)
        estilo_tabla.add('RIGHTPADDING', (i, 0), (i, 0), 0.15*cm)
        estilo_tabla.add('TOPPADDING', (i, 0), (i, 0), 0.15*cm)
        estilo_tabla.add('BOTTOMPADDING', (i, 0), (i, 0), 0.15*cm)
    
    return estilo_tabla

def aplicar_colores_alternos(estilo_tabla, num_filas):
    """
    Aplica colores alternos a las filas de la tabla para mejor legibilidad.
    
    Args:
        estilo_tabla: Estilo de tabla al que aplicar los colores alternos
        num_filas: Número de filas en la tabla
        
    Returns:
        TableStyle: Estilo de tabla actualizado
    """
    for i in range(1, num_filas):
        if i % 2 == 1:  # Filas impares (empezando desde la segunda fila, que es índice 1)
            estilo_tabla.add('BACKGROUND', (0, i), (-1, i), COLOR_GRIS_CLARO)
    return estilo_tabla

def definir_anchos_columnas(num_columnas):
    """
    Define los anchos de columna para la tabla del PDF.
    
    Args:
        num_columnas: Número de columnas en la tabla
        
    Returns:
        list: Lista con los anchos de columna
    """
    # Calcular el ancho disponible en la página A4 vertical (21 cm de ancho)
    # Restando los márgenes izquierdo y derecho (1.5 cm cada uno)
    ancho_disponible = 21.0 - (1.5 * 2)  # 18.0 cm disponibles
    
    # Distribución porcentual de las columnas
    # Primera columna (NOMBRE ORDEN): 25% del espacio
    # Columnas de horas (HORA INICIO, HORA FIN): 8% cada una
    # Columna SECC.: 11%
    # Resto de columnas: distribuir el 48% restante equitativamente
    
    ancho_nombre_orden = ancho_disponible * 0.25  # 25% para NOMBRE ORDEN
    ancho_horas = ancho_disponible * 0.08  # 8% para cada columna de horas
    ancho_secc = ancho_disponible * 0.11  # 11% para SECC.
    
    # Calcular el espacio restante para las columnas intermedias
    espacio_restante = ancho_disponible - ancho_nombre_orden - (ancho_horas * 2) - ancho_secc
    
    # Calcular el ancho de cada columna intermedia (hay num_columnas - 4 columnas intermedias)
    # Las 4 columnas especiales son: NOMBRE ORDEN, HORA INICIO, HORA FIN y SECC.
    if num_columnas > 4:
        ancho_columnas_intermedias = espacio_restante / (num_columnas - 4)
    else:
        ancho_columnas_intermedias = 0
    
    # Crear la lista de anchos de columna
    anchos_columnas = [ancho_nombre_orden * cm]  # NOMBRE ORDEN
    
    # Añadir columnas intermedias
    for i in range(num_columnas - 4):
        anchos_columnas.append(ancho_columnas_intermedias * cm)
    
    # Añadir columnas de horas y SECC.
    anchos_columnas.extend([ancho_horas * cm, ancho_horas * cm])  # HORA INICIO, HORA FIN
    anchos_columnas.append(ancho_secc * cm)  # SECC.
    
    return anchos_columnas
