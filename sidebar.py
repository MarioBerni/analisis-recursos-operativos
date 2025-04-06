"""
Módulo para la barra lateral de la aplicación Streamlit.
"""

import streamlit as st

def configurar_sidebar(SIDEBAR_INFO, UNIDADES_ORDEN, UNIDADES_NOMBRES, COPYRIGHT):
    """
    Configura la barra lateral de la aplicación.
    
    Args:
        SIDEBAR_INFO (str): Información para mostrar en la barra lateral.
        UNIDADES_ORDEN (list): Lista ordenada de unidades.
        UNIDADES_NOMBRES (dict): Diccionario con los nombres de las unidades.
        COPYRIGHT (str): Texto de copyright.
    """
    # Logo
    st.sidebar.image("images/logo-gr-dorado.svg", width=150)
    
    # Información del sistema
    st.sidebar.header("Información del Sistema")
    st.sidebar.markdown("""<div class='sidebar-card'>
    <p>Esta aplicación permite generar reportes PDF a partir de archivos Excel con información de despliegues operativos de la Guardia Republicana.</p>
    </div>""", unsafe_allow_html=True)
    
    # Información sobre las hojas esperadas
    st.sidebar.markdown("### Hojas del Excel")
    st.sidebar.markdown("""<div class='sidebar-card'>
    <ul>
    <li><strong>OPERATIVOS:</strong> Información general</li>
    <li><strong>01-31:</strong> Datos diarios del mes</li>
    </ul>
    </div>""", unsafe_allow_html=True)
    
    # Información sobre las unidades
    st.sidebar.markdown("### Unidades")
    st.sidebar.markdown("""<div class='sidebar-card'>
    <strong>Organización por unidades:</strong>
    <ul>
    """ + "".join([f"<li><strong>{unidad}:</strong> {UNIDADES_NOMBRES[unidad]}</li>" for unidad in UNIDADES_ORDEN]) + """
    </ul>
    </div>""", unsafe_allow_html=True)
    
    # Ayuda rápida
    st.sidebar.markdown("### Ayuda rápida")
    st.sidebar.markdown("""<div class='sidebar-card'>
    <ol>
    <li>Cargue un archivo Excel</li>
    <li>Seleccione las opciones de organización</li>
    <li>Revise la vista previa de los datos</li>
    <li>Genere y descargue el PDF</li>
    </ol>
    </div>""", unsafe_allow_html=True)
    
    # Pie de página
    st.sidebar.markdown("---")
    st.sidebar.markdown(f'<div class="footer">{COPYRIGHT}<br>Versión 1.0.0</div>', unsafe_allow_html=True)
