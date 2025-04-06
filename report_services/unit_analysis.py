"""
Módulo para el análisis por unidad en los reportes de cumplimiento.
"""

import pandas as pd
from reportlab.platypus import Paragraph, Spacer, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.units import cm
from charts import crear_grafica_barras, crear_grafica_pastel

from report_services.utils import crear_tabla_con_estilo

def generar_analisis_por_unidad(df, estilos, estilos_parrafo):
    """
    Genera el análisis por unidad para el reporte de cumplimiento.
    
    Args:
        df (pandas.DataFrame): DataFrame con los datos de despliegues operativos.
        estilos (dict): Diccionario con los estilos para las tablas.
        estilos_parrafo (dict): Diccionario con los estilos para los párrafos.
        
    Returns:
        list: Lista de elementos para el PDF (párrafos, tablas, etc.).
    """
    elementos = []
    
    # Verificar si existe la columna UNIDAD
    if 'UNIDAD' not in df.columns:
        return elementos
    
    # Título de la sección
    elementos.append(Paragraph("ANÁLISIS POR UNIDAD", estilos_parrafo['subtitle']))
    elementos.append(Spacer(1, 0.3*cm))
    
    # Agrupar por unidad
    df_unidad = df.groupby('UNIDAD').agg({
        'NOMBRE OPERATIVO': 'count',
        'PP.SS TOTAL': 'sum',
        'MOVILES': 'sum',
        'MOTOS': 'sum'
    }).reset_index()
    
    # Renombrar columnas
    df_unidad = df_unidad.rename(columns={
        'NOMBRE OPERATIVO': 'SERVICIOS',
        'PP.SS TOTAL': 'PERSONAL',
        'MOVILES': 'MÓVILES'
    })
    
    # Ordenar por cantidad de servicios (descendente)
    df_unidad = df_unidad.sort_values('SERVICIOS', ascending=False)
    
    # Crear datos para la tabla
    datos_unidad = []
    for _, row in df_unidad.iterrows():
        datos_unidad.append([
            row['UNIDAD'],
            row['SERVICIOS'],
            row['PERSONAL'],
            row['MÓVILES'],
            row['MOTOS']
        ])
    
    # Añadir fila de totales
    datos_unidad.append([
        "TOTAL",
        df_unidad['SERVICIOS'].sum(),
        df_unidad['PERSONAL'].sum(),
        df_unidad['MÓVILES'].sum(),
        df_unidad['MOTOS'].sum()
    ])
    
    # Crear tabla
    encabezados = ["UNIDAD", "SERVICIOS", "PERSONAL", "MÓVILES", "MOTOS"]
    tabla_unidad = crear_tabla_con_estilo(
        datos_unidad, 
        encabezados, 
        colWidths=[8*cm, 3*cm, 3*cm, 3*cm, 3*cm]
    )
    
    elementos.append(tabla_unidad)
    elementos.append(Spacer(1, 0.5*cm))
    
    # Gráficas de distribución por unidad
    elementos.extend(generar_graficas_por_unidad(df_unidad))
    
    return elementos

def generar_graficas_por_unidad(df_unidad):
    """
    Genera gráficas para el análisis por unidad.
    
    Args:
        df_unidad (pandas.DataFrame): DataFrame agrupado por unidad.
        
    Returns:
        list: Lista de elementos gráficos para el PDF.
    """
    elementos = []
    
    # Gráfica de servicios por unidad
    servicios_por_unidad = dict(zip(df_unidad['UNIDAD'], df_unidad['SERVICIOS']))
    grafica_servicios = crear_grafica_barras(
        servicios_por_unidad,
        "Servicios por Unidad"
    )
    elementos.append(grafica_servicios)
    elementos.append(Spacer(1, 0.5*cm))
    
    # Gráfica de personal por unidad
    personal_por_unidad = dict(zip(df_unidad['UNIDAD'], df_unidad['PERSONAL']))
    grafica_personal = crear_grafica_barras(
        personal_por_unidad,
        "Personal por Unidad"
    )
    elementos.append(grafica_personal)
    elementos.append(Spacer(1, 0.5*cm))
    
    # Gráfica de distribución de servicios (pastel)
    grafica_distribucion = crear_grafica_pastel(
        servicios_por_unidad,
        "Distribución de Servicios por Unidad"
    )
    elementos.append(grafica_distribucion)
    elementos.append(Spacer(1, 1*cm))
    
    return elementos
