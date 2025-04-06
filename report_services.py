"""
Módulo para la generación de reportes de cumplimiento de servicios.
"""

import pandas as pd
from datetime import datetime
from reportlab.platypus import Paragraph, Spacer, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.units import cm
from reportlab.lib.styles import getSampleStyleSheet

def crear_reporte_cumplimiento(df, estilos):
    """
    Crea un reporte de cumplimiento de servicios a partir de un DataFrame.
    
    Args:
        df (pandas.DataFrame): DataFrame con los datos de despliegues operativos.
        estilos (dict): Diccionario con los estilos para las tablas.
        
    Returns:
        list: Lista de elementos para el PDF (párrafos, tablas, etc.).
    """
    # Lista de elementos para el PDF
    elementos = []
    
    # Estilos para párrafos
    styles = getSampleStyleSheet()
    title_style = styles['Heading1']
    title_style.alignment = 1  # Centrado
    title_style.textColor = colors.Color(0.8, 0.6, 0.0)  # Color dorado
    
    subtitle_style = styles['Heading2']
    subtitle_style.alignment = 1  # Centrado
    
    normal_style = styles['Normal']
    
    # Título del reporte
    elementos.append(Paragraph("REPORTE DE CUMPLIMIENTO DE SERVICIOS", title_style))
    elementos.append(Spacer(1, 0.5*cm))
    
    # Fecha actual
    fecha_actual = datetime.now().strftime("%d de %B de %Y").replace("January", "Enero").replace("February", "Febrero").replace("March", "Marzo").replace("April", "Abril").replace("May", "Mayo").replace("June", "Junio").replace("July", "Julio").replace("August", "Agosto").replace("September", "Septiembre").replace("October", "Octubre").replace("November", "Noviembre").replace("December", "Diciembre")
    elementos.append(Paragraph(f"Fecha de generación: {fecha_actual}", normal_style))
    elementos.append(Spacer(1, 0.5*cm))
    
    # Resumen general
    elementos.append(Paragraph("RESUMEN GENERAL", subtitle_style))
    elementos.append(Spacer(1, 0.3*cm))
    
    # Calcular estadísticas generales
    total_servicios = len(df)
    total_personal = df['PP.SS TOTAL'].sum() if 'PP.SS TOTAL' in df.columns else 0
    total_moviles = df['MOVILES'].sum() if 'MOVILES' in df.columns else 0
    total_motos = df['MOTOS'].sum() if 'MOTOS' in df.columns else 0
    
    # Crear tabla de resumen general
    datos_resumen = [
        ["CONCEPTO", "CANTIDAD"],
        ["Total de Servicios", total_servicios],
        ["Total de Personal", total_personal],
        ["Total de Móviles", total_moviles],
        ["Total de Motos", total_motos]
    ]
    
    tabla_resumen = Table(datos_resumen, colWidths=[10*cm, 5*cm])
    tabla_resumen.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (1, 0), colors.Color(0.8, 0.6, 0.0)),  # Color dorado para encabezado
        ('TEXTCOLOR', (0, 0), (1, 0), colors.white),
        ('ALIGN', (0, 0), (1, 0), 'CENTER'),
        ('FONTNAME', (0, 0), (1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (1, 0), 5),
        ('BACKGROUND', (0, 1), (1, -1), colors.white),
        ('GRID', (0, 0), (1, -1), 1, colors.black),
        ('ALIGN', (1, 1), (1, -1), 'CENTER'),
    ]))
    
    elementos.append(tabla_resumen)
    elementos.append(Spacer(1, 0.5*cm))
    
    # Análisis por unidad si existe la columna UNIDAD
    if 'UNIDAD' in df.columns:
        elementos.append(Paragraph("CUMPLIMIENTO POR UNIDAD", subtitle_style))
        elementos.append(Spacer(1, 0.3*cm))
        
        # Agrupar por unidad
        df_unidades = df.groupby('UNIDAD').agg({
            'NOMBRE OPERATIVO': 'count',
            'PP.SS TOTAL': 'sum',
            'MOVILES': 'sum',
            'MOTOS': 'sum'
        }).reset_index()
        
        # Renombrar columnas
        df_unidades = df_unidades.rename(columns={
            'NOMBRE OPERATIVO': 'SERVICIOS',
            'PP.SS TOTAL': 'PERSONAL',
            'MOVILES': 'MÓVILES',
            'MOTOS': 'MOTOS'
        })
        
        # Importar orden de unidades
        from unidades_config import UNIDADES_ORDEN, UNIDADES_NOMBRES
        
        # Ordenar según el orden definido
        df_unidades['ORDEN'] = df_unidades['UNIDAD'].map({unidad: i for i, unidad in enumerate(UNIDADES_ORDEN)})
        df_unidades = df_unidades.sort_values('ORDEN').drop('ORDEN', axis=1)
        
        # Reemplazar códigos de unidad por nombres completos
        df_unidades['UNIDAD'] = df_unidades['UNIDAD'].map(UNIDADES_NOMBRES)
        
        # Crear tabla de unidades
        datos_unidades = [["UNIDAD", "SERVICIOS", "PERSONAL", "MÓVILES", "MOTOS"]]
        for _, row in df_unidades.iterrows():
            datos_unidades.append([
                row['UNIDAD'],
                row['SERVICIOS'],
                row['PERSONAL'],
                row['MÓVILES'],
                row['MOTOS']
            ])
        
        # Añadir fila de totales
        datos_unidades.append([
            "TOTAL",
            df_unidades['SERVICIOS'].sum(),
            df_unidades['PERSONAL'].sum(),
            df_unidades['MÓVILES'].sum(),
            df_unidades['MOTOS'].sum()
        ])
        
        tabla_unidades = Table(datos_unidades, colWidths=[8*cm, 3*cm, 3*cm, 3*cm, 3*cm])
        tabla_unidades.setStyle(TableStyle([
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
        
        elementos.append(tabla_unidades)
        elementos.append(Spacer(1, 0.5*cm))
    
    # Análisis por tipo de orden si existe la columna TIPO ORDEN
    if 'TIPO ORDEN' in df.columns:
        elementos.append(Paragraph("CUMPLIMIENTO POR TIPO DE ORDEN", subtitle_style))
        elementos.append(Spacer(1, 0.3*cm))
        
        # Agrupar por tipo de orden
        df_tipos = df.groupby('TIPO ORDEN').agg({
            'NOMBRE OPERATIVO': 'count',
            'PP.SS TOTAL': 'sum',
            'MOVILES': 'sum',
            'MOTOS': 'sum'
        }).reset_index()
        
        # Renombrar columnas
        df_tipos = df_tipos.rename(columns={
            'NOMBRE OPERATIVO': 'SERVICIOS',
            'PP.SS TOTAL': 'PERSONAL',
            'MOVILES': 'MÓVILES',
            'MOTOS': 'MOTOS'
        })
        
        # Crear tabla de tipos de orden
        datos_tipos = [["TIPO DE ORDEN", "SERVICIOS", "PERSONAL", "MÓVILES", "MOTOS"]]
        for _, row in df_tipos.iterrows():
            datos_tipos.append([
                row['TIPO ORDEN'],
                row['SERVICIOS'],
                row['PERSONAL'],
                row['MÓVILES'],
                row['MOTOS']
            ])
        
        # Añadir fila de totales
        datos_tipos.append([
            "TOTAL",
            df_tipos['SERVICIOS'].sum(),
            df_tipos['PERSONAL'].sum(),
            df_tipos['MÓVILES'].sum(),
            df_tipos['MOTOS'].sum()
        ])
        
        tabla_tipos = Table(datos_tipos, colWidths=[8*cm, 3*cm, 3*cm, 3*cm, 3*cm])
        tabla_tipos.setStyle(TableStyle([
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
        
        elementos.append(tabla_tipos)
    
    return elementos
