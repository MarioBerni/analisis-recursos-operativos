"""
Módulo para la generación del resumen general de los reportes de cumplimiento.
"""

import pandas as pd
from reportlab.platypus import Paragraph, Spacer, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.units import cm
from charts import crear_grafica_barras, crear_grafica_pastel

from report_services.utils import crear_tabla_con_estilo

def generar_resumen_general(df, estilos, estilos_parrafo):
    """
    Genera el resumen general del reporte de cumplimiento.
    
    Args:
        df (pandas.DataFrame): DataFrame con los datos de despliegues operativos.
        estilos (dict): Diccionario con los estilos para las tablas.
        estilos_parrafo (dict): Diccionario con los estilos para los párrafos.
        
    Returns:
        list: Lista de elementos para el PDF (párrafos, tablas, etc.).
    """
    elementos = []
    
    # Título de la sección
    elementos.append(Paragraph("RESUMEN GENERAL", estilos_parrafo['subtitle']))
    elementos.append(Spacer(1, 0.3*cm))
    
    # Calcular estadísticas generales
    total_servicios = len(df)
    total_personal = df['PP.SS TOTAL'].sum() if 'PP.SS TOTAL' in df.columns else 0
    total_moviles = df['MOVILES'].sum() if 'MOVILES' in df.columns else 0
    total_motos = df['MOTOS'].sum() if 'MOTOS' in df.columns else 0
    
    # Crear tabla de resumen general
    datos_resumen = [
        ["Total de Servicios", str(total_servicios)],
        ["Total de Personal", str(int(total_personal))],
        ["Total de Móviles", str(int(total_moviles))],
        ["Total de Motos", str(int(total_motos))]
    ]
    
    tabla_resumen = Table(datos_resumen, colWidths=[8*cm, 8*cm])
    tabla_resumen.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.Color(0.8, 0.6, 0.0)),  # Color dorado para primera columna
        ('TEXTCOLOR', (0, 0), (0, -1), colors.white),
        ('ALIGN', (0, 0), (0, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (0, -1), 12),
        ('BACKGROUND', (1, 0), (1, -1), colors.white),
        ('ALIGN', (1, 0), (1, -1), 'CENTER'),
        ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
        ('FONTSIZE', (1, 0), (1, -1), 12),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    
    elementos.append(tabla_resumen)
    elementos.append(Spacer(1, 0.5*cm))
    
    # Generar gráficas de resumen si hay datos suficientes
    if total_servicios > 0:
        elementos.extend(generar_graficas_resumen(df))
    
    return elementos

def generar_graficas_resumen(df):
    """
    Genera gráficas para el resumen general.
    
    Args:
        df (pandas.DataFrame): DataFrame con los datos de despliegues operativos.
        
    Returns:
        list: Lista de elementos gráficos para el PDF.
    """
    elementos = []
    
    # Distribución de personal por tipo (en móvil vs pie tierra)
    if all(col in df.columns for col in ['PP.SS EN MOVIL', 'PP.SS PIE TIERRA']):
        total_en_movil = df['PP.SS EN MOVIL'].sum()
        total_pie_tierra = df['PP.SS PIE TIERRA'].sum()
        
        if total_en_movil > 0 or total_pie_tierra > 0:
            distribucion_personal = {
                'En Móvil': total_en_movil,
                'Pie Tierra': total_pie_tierra
            }
            
            grafica_distribucion = crear_grafica_pastel(
                distribucion_personal,
                "Distribución de Personal"
            )
            elementos.append(grafica_distribucion)
            elementos.append(Spacer(1, 0.5*cm))
    
    # Distribución de servicios por tipo de choque
    if all(col in df.columns for col in ['CHOQUE APOSTADO', 'CHOQUE ALERTA']):
        total_choque_apostado = df['CHOQUE APOSTADO'].sum()
        total_choque_alerta = df['CHOQUE ALERTA'].sum()
        
        if total_choque_apostado > 0 or total_choque_alerta > 0:
            distribucion_choque = {
                'Choque Apostado': total_choque_apostado,
                'Choque Alerta': total_choque_alerta
            }
            
            grafica_choque = crear_grafica_pastel(
                distribucion_choque,
                "Distribución por Tipo de Choque"
            )
            elementos.append(grafica_choque)
            elementos.append(Spacer(1, 0.5*cm))
    
    # Distribución de servicios por tipo GEO
    if all(col in df.columns for col in ['GEO APOSTADO', 'GEO ALERTA']):
        total_geo_apostado = df['GEO APOSTADO'].sum()
        total_geo_alerta = df['GEO ALERTA'].sum()
        
        if total_geo_apostado > 0 or total_geo_alerta > 0:
            distribucion_geo = {
                'GEO Apostado': total_geo_apostado,
                'GEO Alerta': total_geo_alerta
            }
            
            grafica_geo = crear_grafica_pastel(
                distribucion_geo,
                "Distribución por Tipo GEO"
            )
            elementos.append(grafica_geo)
            elementos.append(Spacer(1, 1*cm))
    
    return elementos
