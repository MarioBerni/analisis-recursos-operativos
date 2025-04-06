"""
Módulo para la generación de reportes de cumplimiento de servicios.
"""

import pandas as pd
from datetime import datetime
from reportlab.platypus import Paragraph, Spacer, Table, TableStyle, KeepTogether
from reportlab.lib import colors
from reportlab.lib.units import cm
from reportlab.lib.styles import getSampleStyleSheet

# Importar módulo de gráficas modularizado
from charts import (
    crear_grafica_barras,
    crear_grafica_pastel,
    crear_grafica_lineas_tiempo,
    crear_grafica_comparativa
)

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
        return [Paragraph("No hay datos disponibles para generar el reporte.", getSampleStyleSheet()['Normal'])]
        
    # Asegurar que las columnas numéricas sean de tipo numérico
    columnas_numericas = ['PP.SS TOTAL', 'MOVILES', 'MOTOS', 'PERSONAL', 'SS.OO', 'HIPO', 
                        'PP.SS EN MOVIL', 'PP.SS PIE TIERRA', 'CHOQUE APOSTADO', 
                        'CHOQUE ALERTA', 'GEO APOSTADO', 'GEO ALERTA']
    
    for col in columnas_numericas:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
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
    
    # Fecha actual para la generación del reporte
    fecha_actual = datetime.now().strftime("%d de %B de %Y").replace("January", "Enero").replace("February", "Febrero").replace("March", "Marzo").replace("April", "Abril").replace("May", "Mayo").replace("June", "Junio").replace("July", "Julio").replace("August", "Agosto").replace("September", "Septiembre").replace("October", "Octubre").replace("November", "Noviembre").replace("December", "Diciembre")
    
    # Usar el mes y año seleccionados o los actuales si no se proporcionaron
    if mes is None:
        mes = datetime.now().strftime("%B").replace("January", "Enero").replace("February", "Febrero").replace("March", "Marzo").replace("April", "Abril").replace("May", "Mayo").replace("June", "Junio").replace("July", "Julio").replace("August", "Agosto").replace("September", "Septiembre").replace("October", "Octubre").replace("November", "Noviembre").replace("December", "Diciembre")
    
    if año is None:
        año = datetime.now().year
    
    # Añadir información del periodo y fecha de generación
    elementos.append(Paragraph(f"<b>Periodo:</b> {mes} {año}", normal_style))
    elementos.append(Paragraph(f"<b>Fecha de generación:</b> {fecha_actual}", normal_style))
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
        
        # Ordenar unidades según configuración
        df_unidades['orden'] = df_unidades['UNIDAD'].map({unidad: i for i, unidad in enumerate(UNIDADES_ORDEN)})
        df_unidades = df_unidades.sort_values('orden').drop('orden', axis=1)
        
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
        
        # Crear gráficas para unidades
        elementos.append(Paragraph("GRÁFICAS POR UNIDAD", subtitle_style))
        elementos.append(Spacer(1, 0.3*cm))
        
        # Gráfica de barras para servicios por unidad
        servicios_por_unidad = dict(zip(df_unidades['UNIDAD'], df_unidades['SERVICIOS']))
        grafica_servicios = crear_grafica_barras(
            servicios_por_unidad,
            "Servicios por Unidad",
            "Unidad",
            "Cantidad de Servicios"
        )
        elementos.append(grafica_servicios)
        elementos.append(Spacer(1, 0.5*cm))
        
        # Gráfica de pastel para distribución de personal
        personal_por_unidad = dict(zip(df_unidades['UNIDAD'], df_unidades['PERSONAL']))
        grafica_personal = crear_grafica_pastel(
            personal_por_unidad,
            "Distribución de Personal por Unidad"
        )
        elementos.append(grafica_personal)
        elementos.append(Spacer(1, 0.5*cm))
        
        # Gráfica comparativa de recursos por unidad
        recursos_por_unidad = {}
        for _, row in df_unidades.iterrows():
            unidad = row['UNIDAD']
            recursos_por_unidad[unidad] = {
                'Personal': row['PERSONAL'],
                'Móviles': row['MÓVILES'],
                'Motos': row['MOTOS']
            }
        
        grafica_recursos = crear_grafica_comparativa(
            recursos_por_unidad,
            "Comparativa de Recursos por Unidad",
            "Unidad",
            "Cantidad"
        )
        elementos.append(grafica_recursos)
        elementos.append(Spacer(1, 1*cm))
    
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
        elementos.append(Spacer(1, 0.5*cm))
        
        # Crear gráficas para tipos de orden
        elementos.append(Paragraph("GRÁFICAS POR TIPO DE ORDEN", subtitle_style))
        elementos.append(Spacer(1, 0.3*cm))
        
        # Gráfica de barras para servicios por tipo de orden
        servicios_por_tipo = dict(zip(df_tipos['TIPO ORDEN'], df_tipos['SERVICIOS']))
        grafica_servicios_tipo = crear_grafica_barras(
            servicios_por_tipo,
            "Servicios por Tipo de Orden",
            "Tipo de Orden",
            "Cantidad de Servicios"
        )
        elementos.append(grafica_servicios_tipo)
        elementos.append(Spacer(1, 0.5*cm))
        
        # Gráfica de pastel para distribución de personal por tipo de orden
        personal_por_tipo = dict(zip(df_tipos['TIPO ORDEN'], df_tipos['PERSONAL']))
        grafica_personal_tipo = crear_grafica_pastel(
            personal_por_tipo,
            "Distribución de Personal por Tipo de Orden"
        )
        elementos.append(grafica_personal_tipo)
        elementos.append(Spacer(1, 1*cm))
    
    # Análisis por tipo operativo si existe la columna TIPO OPERATIVO
    if 'TIPO OPERATIVO' in df.columns:
        elementos.append(Paragraph("ANÁLISIS POR TIPO OPERATIVO", subtitle_style))
        elementos.append(Spacer(1, 0.3*cm))
        
        # Agrupar por tipo operativo
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
            'MOVILES': 'MÓVILES',
            'MOTOS': 'MOTOS'
        })
        
        # Crear tabla de tipos operativos
        datos_tipo_op = [["TIPO OPERATIVO", "SERVICIOS", "PERSONAL", "MÓVILES", "MOTOS"]]
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
        
        tabla_tipo_op = Table(datos_tipo_op, colWidths=[8*cm, 3*cm, 3*cm, 3*cm, 3*cm])
        tabla_tipo_op.setStyle(TableStyle([
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
    
    # Análisis temporal si existe la columna FECHA
    if 'FECHA' in df.columns:
        elementos.append(Paragraph("EVOLUCIÓN TEMPORAL DE SERVICIOS", subtitle_style))
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
