"""
Generador de PDFs para despliegues operativos - Versión modular y optimizada.
"""

import io
import pandas as pd
from reportlab.platypus import SimpleDocTemplate

# Importar módulos propios
from config import PDF_TITLE
from pdf_config import COLUMNAS_PDF
from pdf_header_footer import encabezado_pie_pagina
from data_utils import preparar_dataframe, clasificar_datos_por_unidad
from table_elements import crear_tabla_por_unidad, crear_tabla_general
from table_styles import crear_estilos_tabla

def crear_documento_pdf(buffer):
    """
    Crea un documento PDF con la configuración de márgenes y metadatos adecuados.
    
    Args:
        buffer (io.BytesIO): Buffer donde se escribirá el PDF.
        
    Returns:
        SimpleDocTemplate: Documento PDF configurado.
    """
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.units import cm
    
    return SimpleDocTemplate(
        buffer,
        pagesize=A4,  # Orientación vertical (portrait)
        title=PDF_TITLE,
        author="Sistema de Despliegues Operativos",
        leftMargin=1.5*cm,  # Margen izquierdo ampliado
        rightMargin=1.5*cm,  # Margen derecho ampliado
        topMargin=3.0*cm,  # Margen superior reducido
        bottomMargin=2.0*cm  # Margen inferior para el pie de página
    )

def generar_pdf_optimizado(df, organizar_por_unidad=True, reporte_cumplimiento=False):
    """
    Genera un PDF optimizado a partir de un DataFrame con datos de despliegues operativos.
    
    El PDF puede organizarse por unidades o mostrar todos los datos en una sola tabla.
    Incluye encabezados personalizados, imágenes para algunas columnas, y estilos 
    definidos para mejorar la legibilidad.
    
    Args:
        df (pandas.DataFrame): DataFrame con los datos de despliegues operativos.
        organizar_por_unidad (bool, optional): Si es True, organiza las tablas por unidad.
            Defaults to True.
        reporte_cumplimiento (bool, optional): Si es True, genera un reporte de cumplimiento de servicios.
            Defaults to False.
        
    Returns:
        bytes: PDF generado en formato bytes, listo para ser descargado o mostrado.
        
    Raises:
        ValueError: Si el DataFrame está vacío o no contiene las columnas necesarias.
    """
    # Verificar si el DataFrame está vacío
    if df.empty:
        raise ValueError("El DataFrame está vacío. No se puede generar el PDF.")
        
    # Verificar si la columna UNIDAD existe, si no, desactivar la organización por unidad
    if 'UNIDAD' not in df.columns:
        organizar_por_unidad = False
        print("Advertencia: La columna 'UNIDAD' no existe en el DataFrame. Se desactivará la organización por unidad.")
    
    # Preparar el DataFrame para el PDF
    df_completo, df_filtrado, columnas_disponibles = preparar_dataframe(df)
    
    # Crear buffer para el PDF
    buffer = io.BytesIO()
    
    # Crear documento PDF
    doc = crear_documento_pdf(buffer)
    
    # Crear estilos
    estilos = crear_estilos_tabla()
    
    # Lista de elementos para el PDF
    elementos = []
    
    # Si se solicita un reporte de cumplimiento de servicios
    if reporte_cumplimiento:
        # Importar función para crear el reporte de cumplimiento
        from report_services import crear_reporte_cumplimiento
        elementos.extend(crear_reporte_cumplimiento(df_completo, estilos))
    # Si se organiza por unidad, crear tablas separadas para cada unidad
    elif organizar_por_unidad and 'UNIDAD' in df_completo.columns:
        # Clasificar datos por unidad
        dfs_por_unidad = clasificar_datos_por_unidad(df_completo, df_filtrado)
        
        # Importar orden de unidades
        from unidades_config import UNIDADES_ORDEN
        
        # Para cada unidad en el orden definido
        for unidad in UNIDADES_ORDEN:
            # Si hay datos para esta unidad, crear una tabla
            if unidad in dfs_por_unidad:
                df_unidad = dfs_por_unidad[unidad]
                # Usar la función crear_tabla_por_unidad para generar la tabla y agregarla a los elementos
                elementos.extend(crear_tabla_por_unidad(unidad, df_unidad, columnas_disponibles, estilos))
    else:
        # Si no se organiza por unidad, crear una sola tabla con todos los datos
        elementos.extend(crear_tabla_general(df_filtrado, columnas_disponibles, estilos))
    
    # Construir documento con encabezado y pie de página
    doc.build(elementos, onFirstPage=encabezado_pie_pagina, onLaterPages=encabezado_pie_pagina)
    
    # Obtener contenido del buffer
    buffer.seek(0)
    return buffer.getvalue()
