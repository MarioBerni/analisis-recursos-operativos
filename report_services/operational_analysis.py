"""
Módulo para el análisis por tipo de operativo en los reportes de cumplimiento.
"""

import pandas as pd
from reportlab.platypus import Paragraph, Spacer, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.units import cm
from charts import crear_grafica_barras, crear_grafica_pastel

from report_services.utils import crear_tabla_con_estilo

def generar_analisis_por_tipo_operativo(df, estilos, estilos_parrafo):
    """
    Genera el análisis por tipo de operativo para el reporte de cumplimiento.
    
    Args:
        df (pandas.DataFrame): DataFrame con los datos de despliegues operativos.
        estilos (dict): Diccionario con los estilos para las tablas.
        estilos_parrafo (dict): Diccionario con los estilos para los párrafos.
        
    Returns:
        list: Lista de elementos para el PDF (párrafos, tablas, etc.).
    """
    elementos = []
    
    # Verificar si existe la columna TIPO OPERATIVO
    if 'TIPO OPERATIVO' not in df.columns:
        return elementos
    
    # Título de la sección
    elementos.append(Paragraph("ANÁLISIS POR TIPO DE OPERATIVO", estilos_parrafo['subtitle']))
    elementos.append(Spacer(1, 0.3*cm))
    
    # Agrupar por tipo de operativo
    df_tipo_op = df.groupby('TIPO OPERATIVO').agg({
        'NOMBRE OPERATIVO': 'count',
        'PP.SS TOTAL': 'sum',
        'MOVILES': 'sum',
        'MOTOS': 'sum'
    }).reset_index()
    
    # Renombrar columnas
    df_tipo_op = df_tipo_op.rename(columns={
        'NOMBRE OPERATIVO': 'SERVICIOS',
        'PP.SS TOTAL': 'PERSONAL',
        'MOVILES': 'MÓVILES'
    })
    
    # Ordenar por cantidad de servicios (descendente)
    df_tipo_op = df_tipo_op.sort_values('SERVICIOS', ascending=False)
    
    # Crear datos para la tabla
    datos_tipo_op = []
    for _, row in df_tipo_op.iterrows():
        datos_tipo_op.append([
            row['TIPO OPERATIVO'],
            row['SERVICIOS'],
            row['PERSONAL'],
            row['MÓVILES'],
            row['MOTOS']
        ])
    
    # Añadir fila de totales
    datos_tipo_op.append([
        "TOTAL",
        df_tipo_op['SERVICIOS'].sum(),
        df_tipo_op['PERSONAL'].sum(),
        df_tipo_op['MÓVILES'].sum(),
        df_tipo_op['MOTOS'].sum()
    ])
    
    # Crear tabla
    encabezados = ["TIPO OPERATIVO", "SERVICIOS", "PERSONAL", "MÓVILES", "MOTOS"]
    tabla_tipo_op = crear_tabla_con_estilo(
        datos_tipo_op, 
        encabezados, 
        colWidths=[8*cm, 3*cm, 3*cm, 3*cm, 3*cm]
    )
    
    elementos.append(tabla_tipo_op)
    elementos.append(Spacer(1, 0.5*cm))
    
    # Gráfica de pastel para distribución por tipo operativo
    servicios_por_tipo_op = dict(zip(df_tipo_op['TIPO OPERATIVO'], df_tipo_op['SERVICIOS']))
    grafica_tipo_op = crear_grafica_pastel(
        servicios_por_tipo_op,
        "Distribución de Servicios por Tipo Operativo"
    )
    elementos.append(grafica_tipo_op)
    elementos.append(Spacer(1, 1*cm))
    
    return elementos
