"""
Aplicación principal para convertir archivos Excel de despliegues operativos a PDF.
"""

import streamlit as st

# Importar módulos propios
from config import (
    APP_TITLE, 
    APP_ICON, 
    APP_DESCRIPTION, 
    PDF_FILENAME,
    SIDEBAR_INFO,
    COPYRIGHT,
    EXCEL_SHEETS
)
# Importar la nueva implementación optimizada de generación de PDF
from pdf_generator import generar_pdf_optimizado as generar_pdf
from utils import leer_excel, formatear_datos, obtener_hojas_excel
from unidades_config import UNIDADES_ORDEN, UNIDADES_NOMBRES

# Configuración de la página de Streamlit
st.set_page_config(
    page_title=APP_TITLE,
    page_icon=APP_ICON,
    layout="wide"
)

# Título y descripción
st.title(APP_TITLE)
st.markdown(APP_DESCRIPTION)

# Sección para cargar el archivo Excel
st.header("1. Cargar archivo Excel")
uploaded_file = st.file_uploader("Seleccione el archivo Excel con los datos de despliegues operativos", type=['xlsx', 'xls'])

# Sección de opciones de organización
st.header("2. Opciones de organización")
st.subheader("Organizar por:")
organizar_por_unidad = st.checkbox("Unidad", value=True, help="Organiza las tablas por unidad")
reporte_cumplimiento = st.checkbox("Reporte Cumplimiento de Servicios", value=False, help="Genera un reporte de cumplimiento de servicios")

if uploaded_file is not None:
    # Obtener las hojas disponibles en el archivo Excel
    hojas_disponibles, hojas_validas, mensaje_error_hojas = obtener_hojas_excel(uploaded_file)
    
    if hojas_validas:
        # Si hay más de una hoja, mostrar selector
        hoja_seleccionada = 'OPERATIVOS'  # Hoja por defecto
        
        if len(hojas_disponibles) > 1:
            st.subheader("Seleccionar hoja de datos")
            hoja_seleccionada = st.selectbox(
                "Seleccione la hoja que contiene los datos de despliegues operativos",
                options=hojas_disponibles,
                index=hojas_disponibles.index('OPERATIVOS') if 'OPERATIVOS' in hojas_disponibles else 0
            )
        
        # Procesar el archivo cargado con la hoja seleccionada
        df, es_valido, mensaje_error = leer_excel(uploaded_file, hoja=hoja_seleccionada)
        
        if es_valido:
            # Formatear datos si es necesario
            df = formatear_datos(df)
            
            # Mostrar los datos cargados
            st.header("3. Vista previa de los datos")
            st.dataframe(df)
            
            # Botón para generar y descargar el PDF
            st.header("4. Generar y descargar PDF")
            if st.button("Generar PDF"):
                # Generar el PDF con las opciones seleccionadas
                pdf = generar_pdf(df, organizar_por_unidad=organizar_por_unidad, reporte_cumplimiento=reporte_cumplimiento)
                
                # Proporcionar el PDF para descarga
                st.download_button(
                    label="📥 Descargar PDF",
                    data=pdf,
                    file_name=PDF_FILENAME,
                    mime="application/pdf"
                )
                
                st.success("¡PDF generado con éxito! Haga clic en el botón de descarga para obtener el archivo.")
        else:
            st.error(mensaje_error)
    else:
        st.error(mensaje_error_hojas)

# Información adicional en la barra lateral
st.sidebar.header("Información")
st.sidebar.info(SIDEBAR_INFO)

# Información sobre las unidades
if 'UNIDAD' in SIDEBAR_INFO:
    st.sidebar.header("Unidades")
    st.sidebar.info("""
    **Organización por unidades:**
    """ + "\n".join([f"- {unidad}: {UNIDADES_NOMBRES[unidad]}" for unidad in UNIDADES_ORDEN]))

st.sidebar.markdown("---")
st.sidebar.markdown(COPYRIGHT)
