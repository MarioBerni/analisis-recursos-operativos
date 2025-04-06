"""
Módulo para el análisis temporal en los reportes de cumplimiento.
"""

import pandas as pd
from reportlab.platypus import Paragraph, Spacer
from reportlab.lib.units import cm
from charts import crear_grafica_lineas_tiempo

def generar_analisis_temporal(df, estilos_parrafo):
    """
    Genera el análisis temporal para el reporte de cumplimiento.
    
    Args:
        df (pandas.DataFrame): DataFrame con los datos de despliegues operativos.
        estilos_parrafo (dict): Diccionario con los estilos para los párrafos.
        
    Returns:
        list: Lista de elementos para el PDF (párrafos, tablas, etc.).
    """
    elementos = []
    
    # Verificar si existe la columna FECHA
    if 'FECHA' not in df.columns:
        return elementos
    
    # Título de la sección
    elementos.append(Paragraph("EVOLUCIÓN TEMPORAL DE SERVICIOS", estilos_parrafo['subtitle']))
    elementos.append(Spacer(1, 0.3*cm))
    
    # Convertir FECHA a datetime si no lo es
    if not pd.api.types.is_datetime64_any_dtype(df['FECHA']):
        df['FECHA'] = pd.to_datetime(df['FECHA'], errors='coerce')
    
    # Agrupar por fecha
    df_fechas = df.groupby(df['FECHA'].dt.date).agg({
        'NOMBRE OPERATIVO': 'count',
        'PP.SS TOTAL': 'sum'
    }).reset_index()
    
    # Renombrar columnas
    df_fechas = df_fechas.rename(columns={
        'NOMBRE OPERATIVO': 'SERVICIOS',
        'PP.SS TOTAL': 'PERSONAL'
    })
    
    # Ordenar por fecha
    df_fechas = df_fechas.sort_values('FECHA')
    
    # Convertir fechas a formato string para la gráfica
    fechas_str = [fecha.strftime('%d/%m/%Y') for fecha in df_fechas['FECHA']]
    
    # Crear diccionario para la gráfica
    servicios_por_fecha = dict(zip(fechas_str, df_fechas['SERVICIOS']))
    personal_por_fecha = dict(zip(fechas_str, df_fechas['PERSONAL']))
    
    # Gráfica de líneas para evolución de servicios
    if len(servicios_por_fecha) > 1:  # Solo si hay más de una fecha
        grafica_evolucion = crear_grafica_lineas_tiempo(
            servicios_por_fecha,
            "Evolución de Servicios por Fecha",
            "Fecha",
            "Cantidad de Servicios"
        )
        elementos.append(grafica_evolucion)
        elementos.append(Spacer(1, 0.5*cm))
        
        # Gráfica de líneas para evolución de personal
        grafica_personal_tiempo = crear_grafica_lineas_tiempo(
            personal_por_fecha,
            "Evolución de Personal Asignado por Fecha",
            "Fecha",
            "Cantidad de Personal"
        )
        elementos.append(grafica_personal_tiempo)
        elementos.append(Spacer(1, 0.5*cm))
    
    return elementos
