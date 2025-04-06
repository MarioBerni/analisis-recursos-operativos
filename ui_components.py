"""
Módulo para los componentes de la interfaz de usuario de la aplicación Streamlit.
"""

import streamlit as st
from datetime import datetime
import pandas as pd

from ui_styles import mostrar_info, mostrar_exito, mostrar_error

def mostrar_fecha_actual():
    """
    Muestra la fecha actual formateada en español.
    """
    # Obtener fecha actual
    now = datetime.now()
    # Formatear fecha
    fecha_formato = now.strftime("%d de %B de %Y")
    # Traducir mes al español
    fecha_es = fecha_formato.replace("January", "Enero")
    fecha_es = fecha_es.replace("February", "Febrero")
    fecha_es = fecha_es.replace("March", "Marzo")
    fecha_es = fecha_es.replace("April", "Abril")
    fecha_es = fecha_es.replace("May", "Mayo")
    fecha_es = fecha_es.replace("June", "Junio")
    fecha_es = fecha_es.replace("July", "Julio")
    fecha_es = fecha_es.replace("August", "Agosto")
    fecha_es = fecha_es.replace("September", "Septiembre")
    fecha_es = fecha_es.replace("October", "Octubre")
    fecha_es = fecha_es.replace("November", "Noviembre")
    fecha_es = fecha_es.replace("December", "Diciembre")
    # Mostrar información
    mostrar_info(f"Fecha: {fecha_es}")

def selector_archivo():
    """
    Muestra el selector de archivos Excel.
    
    Returns:
        file: Archivo subido o None.
    """
    col1, col2 = st.columns([3, 1])
    with col1:
        uploaded_file = st.file_uploader(
            "Seleccione el archivo Excel con los datos de despliegues operativos", 
            type=['xlsx', 'xls']
        )
    with col2:
        st.markdown("""<div class='sidebar-card'>
        <h4>Formatos aceptados</h4>
        <ul>
            <li>Excel (.xlsx)</li>
            <li>Excel 97-2003 (.xls)</li>
        </ul>
        </div>""", unsafe_allow_html=True)
    
    return uploaded_file

def opciones_organizacion():
    """
    Muestra las opciones de organización del reporte.
    
    Returns:
        tuple: (organizar_por_unidad, reporte_cumplimiento, mes_seleccionado, año_seleccionado)
    """
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### Tipo de reporte")
        organizar_por_unidad = st.checkbox(
            "Organizar por Unidad", 
            value=True, 
            help="Organiza las tablas por unidad"
        )
        reporte_cumplimiento = st.checkbox(
            "Reporte Cumplimiento de Servicios", 
            value=False, 
            help="Genera un reporte de cumplimiento de servicios"
        )
    
    mes_seleccionado = None
    año_seleccionado = None
    
    if reporte_cumplimiento:
        with col2:
            st.markdown("### Periodo del reporte")
            # Lista de meses en español
            meses = [
                "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
                "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"
            ]
            # Obtener el mes actual (1-12) para seleccionarlo por defecto
            mes_actual = datetime.now().month
            # Selector de mes (índice 0-11, por eso restamos 1 al mes actual)
            mes_seleccionado = st.selectbox(
                "Mes:",
                options=meses,
                index=mes_actual-1,
                help="Seleccione el mes al que corresponden los datos del archivo Excel"
            )
            # Selector de año
            año_actual = datetime.now().year
            año_seleccionado = st.number_input(
                "Año:",
                min_value=2020,
                max_value=2030,
                value=año_actual,
                help="Seleccione el año al que corresponden los datos"
            )
            
            # Mostrar información sobre el reporte
            mostrar_info(f"""
            <strong>Reporte para:</strong> {mes_seleccionado} {año_seleccionado}<br>
            <small>El reporte incluirá gráficos y tablas de resumen.</small>
            """)
    
    return organizar_por_unidad, reporte_cumplimiento, mes_seleccionado, año_seleccionado

def mostrar_vista_previa_datos(df):
    """
    Muestra una vista previa de los datos cargados.
    
    Args:
        df (pandas.DataFrame): DataFrame con los datos.
    """
    # Contenedor para las estadísticas con estilo mejorado
    st.markdown("""<div style='background-color: #092845; padding: 15px; border-radius: 5px; margin-bottom: 20px;'>
    <h4 style='color: #c9a227; margin-top: 0; margin-bottom: 15px;'>Estadísticas de los datos</h4>
    <div style='display: flex; justify-content: space-between;'>
    </div>
    </div>""", unsafe_allow_html=True)
    
    # Mostrar estadísticas básicas
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total de registros", len(df), delta=None, 
                 delta_color="normal", help="Número total de registros en el archivo")
    with col2:
        if 'UNIDAD' in df.columns:
            st.metric("Unidades diferentes", df['UNIDAD'].nunique(), delta=None, 
                     delta_color="normal", help="Número de unidades distintas en los datos")
        else:
            st.metric("Unidades diferentes", "N/A")
    with col3:
        if 'PP.SS TOTAL' in df.columns:
            st.metric("Total personal", int(df['PP.SS TOTAL'].sum()), delta=None, 
                     delta_color="normal", help="Suma total del personal desplegado")
        else:
            st.metric("Total personal", "N/A")
    
    # Mostrar dataframe con opciones de filtrado
    st.markdown("<h4 style='color: #c9a227; margin-top: 20px;'>Vista previa de los datos</h4>", unsafe_allow_html=True)
    st.dataframe(df, height=300, use_container_width=True)

def seccion_generacion_pdf(df, organizar_por_unidad, reporte_cumplimiento, mes_seleccionado, año_seleccionado, PDF_FILENAME):
    """
    Muestra la sección para generar y descargar el PDF.
    
    Args:
        df (pandas.DataFrame): DataFrame con los datos.
        organizar_por_unidad (bool): Si se debe organizar por unidad.
        reporte_cumplimiento (bool): Si se debe generar un reporte de cumplimiento.
        mes_seleccionado (str): Mes seleccionado.
        año_seleccionado (int): Año seleccionado.
        PDF_FILENAME (str): Nombre del archivo PDF.
        
    Returns:
        bool: True si se generó el PDF, False en caso contrario.
    """
    from pdf_generator import generar_pdf_optimizado as generar_pdf
    
    # Contenedor para centrar los botones
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("Generar PDF", key="generar_pdf"):
            # Preparar los parámetros para la generación del PDF
            params = {
                "organizar_por_unidad": organizar_por_unidad,
                "reporte_cumplimiento": reporte_cumplimiento
            }
            
            # Si es un reporte de cumplimiento, añadir mes y año
            if reporte_cumplimiento:
                params["mes"] = mes_seleccionado
                params["año"] = año_seleccionado
            
            # Generar el PDF
            pdf = generar_pdf(df, **params)
            
            # Proporcionar el PDF para descarga
            st.download_button(
                label="📅 Descargar PDF",
                data=pdf,
                file_name=PDF_FILENAME,
                mime="application/pdf",
                key="descargar_pdf"
            )
            
            mostrar_exito("<strong>¡PDF generado con éxito!</strong><br>Haga clic en el botón de descarga para obtener el archivo.")
            
            # Mostrar información sobre el PDF generado
            mostrar_info(f"""
            <strong>Detalles del PDF:</strong><br>
            <ul>
                <li><strong>Nombre:</strong> {PDF_FILENAME}</li>
                <li><strong>Tipo de reporte:</strong> {"Reporte de Cumplimiento" if reporte_cumplimiento else "Reporte por Unidades" if organizar_por_unidad else "Reporte General"}</li>
                <li><strong>Fecha de generación:</strong> {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}</li>
            </ul>
            """)
            
            return True
    
    return False

def mostrar_pie_pagina(COPYRIGHT):
    """
    Muestra el pie de página de la aplicación.
    
    Args:
        COPYRIGHT (str): Texto de copyright.
    """
    st.markdown("---")
    st.markdown('<div class="footer">Desarrollado para la Dirección Nacional Guardia Republicana<br>Estado Mayor Policial - Sección Tecnología</div>', unsafe_allow_html=True)
