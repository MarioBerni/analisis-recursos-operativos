"""
Módulo principal para la generación de reportes de cumplimiento de servicios.
"""

import pandas as pd
from datetime import datetime
from reportlab.platypus import Paragraph, Spacer
from reportlab.lib.units import cm

# Importar módulos propios
from report_services.utils import obtener_estilos_parrafo, obtener_fecha_actual_formateada, obtener_mes_actual_formateado
from report_services.general_summary import generar_resumen_general
from report_services.unit_analysis import generar_analisis_por_unidad
from report_services.operational_analysis import generar_analisis_por_tipo_operativo
from report_services.temporal_analysis import generar_analisis_temporal

def crear_reporte_cumplimiento(df, estilos, mes=None, año=None):
    """
    Crea un reporte de cumplimiento de servicios a partir de un DataFrame.
    
    Args:
        df (pandas.DataFrame): DataFrame con los datos de despliegues operativos.
        estilos (dict): Diccionario con los estilos para las tablas.
        mes (str, optional): Mes al que corresponden los datos (en español).
            Defaults to None (se usará el mes actual).
        año (int, optional): Año al que corresponden los datos.
            Defaults to None (se usará el año actual).
        
    Returns:
        list: Lista de elementos para el PDF (párrafos, tablas, etc.).
    """
    # Verificar si el DataFrame tiene datos
    if df.empty:
        return [Paragraph("No hay datos disponibles para generar el reporte.", obtener_estilos_parrafo()['normal'])]
        
    # Asegurar que las columnas numéricas sean de tipo numérico
    columnas_numericas = ['PP.SS TOTAL', 'MOVILES', 'MOTOS', 'PERSONAL', 'SS.OO', 'HIPO', 
                        'PP.SS EN MOVIL', 'PP.SS PIE TIERRA', 'CHOQUE APOSTADO', 
                        'CHOQUE ALERTA', 'GEO APOSTADO', 'GEO ALERTA']
    
    for col in columnas_numericas:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
    
    # Lista de elementos para el PDF
    elementos = []
    
    # Obtener estilos para párrafos
    estilos_parrafo = obtener_estilos_parrafo()
    
    # Título del reporte
    elementos.append(Paragraph("REPORTE DE CUMPLIMIENTO DE SERVICIOS", estilos_parrafo['title']))
    elementos.append(Spacer(1, 0.5*cm))
    
    # Usar el mes y año seleccionados o los actuales si no se proporcionaron
    if mes is None:
        mes = obtener_mes_actual_formateado()
    
    if año is None:
        año = datetime.now().year
    
    # Añadir información del periodo y fecha de generación
    elementos.append(Paragraph(f"<b>Periodo:</b> {mes} {año}", estilos_parrafo['normal']))
    elementos.append(Paragraph(f"<b>Fecha de generación:</b> {obtener_fecha_actual_formateada()}", estilos_parrafo['normal']))
    elementos.append(Spacer(1, 0.5*cm))
    
    # Generar resumen general
    elementos.extend(generar_resumen_general(df, estilos, estilos_parrafo))
    
    # Generar análisis por unidad
    elementos.extend(generar_analisis_por_unidad(df, estilos, estilos_parrafo))
    
    # Generar análisis por tipo de operativo
    elementos.extend(generar_analisis_por_tipo_operativo(df, estilos, estilos_parrafo))
    
    # Generar análisis temporal
    elementos.extend(generar_analisis_temporal(df, estilos_parrafo))
    
    return elementos
