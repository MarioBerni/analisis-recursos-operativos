"""
Aplicación principal para convertir archivos Excel de despliegues operativos a PDF.
Versión modularizada para mejor mantenibilidad.
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
from unidades_config import UNIDADES_ORDEN, UNIDADES_NOMBRES

# Importar módulos modularizados
from ui_styles import aplicar_estilos, mostrar_encabezado, mostrar_seccion, mostrar_error
from ui_components import mostrar_fecha_actual, selector_archivo, opciones_organizacion, mostrar_vista_previa_datos, seccion_generacion_pdf, mostrar_pie_pagina
from sidebar import configurar_sidebar
from data_processing import procesar_archivo_excel

# Configuración de la página de Streamlit
st.set_page_config(
    page_title=APP_TITLE,
    page_icon=APP_ICON,
    layout="wide",
    initial_sidebar_state="expanded"
)

# Aplicar estilos personalizados
aplicar_estilos()

# Configurar la barra lateral
configurar_sidebar(SIDEBAR_INFO, UNIDADES_ORDEN, UNIDADES_NOMBRES, COPYRIGHT)

# Título y descripción con estilo mejorado
mostrar_encabezado()

# Mostrar la fecha actual
mostrar_fecha_actual()

# Sección 1: Cargar archivo Excel
mostrar_seccion("Cargar archivo Excel", 1)
uploaded_file = selector_archivo()

# Sección 2: Opciones de organización
mostrar_seccion("Opciones de organización", 2)
organizar_por_unidad, reporte_cumplimiento, mes_seleccionado, año_seleccionado = opciones_organizacion()

# Procesar el archivo si se ha cargado
if uploaded_file is not None:
    # Procesar el archivo Excel
    df, mensaje_error = procesar_archivo_excel(uploaded_file, EXCEL_SHEETS)
    
    if df is not None:
        # Sección 3: Vista previa de los datos
        mostrar_seccion("Vista previa de los datos", 3)
        mostrar_vista_previa_datos(df)
        
        # Sección 4: Generar y descargar PDF
        mostrar_seccion("Generar y descargar PDF", 4)
        seccion_generacion_pdf(
            df, 
            organizar_por_unidad, 
            reporte_cumplimiento, 
            mes_seleccionado, 
            año_seleccionado, 
            PDF_FILENAME
        )
    else:
        # Mostrar mensaje de error
        mostrar_error(mensaje_error)

# Pie de página principal
mostrar_pie_pagina(COPYRIGHT)
