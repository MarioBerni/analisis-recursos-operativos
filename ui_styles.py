"""
Módulo para los estilos CSS y configuración visual de la aplicación Streamlit.
"""

import streamlit as st

# Colores institucionales
COLORES = {
    # Colores principales
    "dorado": "#c9a227",
    "azul": "#0d3b66",
    "azul_claro": "#1a5694",
    "azul_oscuro": "#092845",
    
    # Colores neutros
    "blanco": "#ffffff",
    "negro": "#121212",
    "gris_oscuro": "#333333",
    "gris_medio": "#666666",
    "gris_claro": "#f0f0f0",
    
    # Colores de estado
    "verde_oscuro": "#1e7e34",
    "verde": "#28a745",
    "verde_claro": "#e6f3e6",
    "rojo": "#721c24",
    "rojo_claro": "#f8d7da",
    "amarillo": "#ffc107",
    "amarillo_claro": "#fff3cd"
}

def aplicar_estilos():
    """
    Aplica los estilos CSS personalizados a la aplicación Streamlit.
    """
    st.markdown("""
    <style>
        /* Estilos generales */
        body {
            color: #f0f0f0;
            background-color: #121212;
        }
        
        /* Encabezados */
        .main-header {
            color: """ + COLORES["dorado"] + """;
            text-align: center;
            font-weight: bold;
            font-size: 2.5rem;
            margin-bottom: 0;
            padding-bottom: 0;
        }
        .sub-header {
            color: """ + COLORES["azul_claro"] + """;
            text-align: center;
            font-size: 1.2rem;
            margin-top: 0;
            padding-top: 0;
            margin-bottom: 2rem;
        }
        .section-header {
            background-color: """ + COLORES["azul"] + """;
            color: white;
            padding: 10px;
            border-radius: 5px;
            margin-top: 20px;
            margin-bottom: 10px;
        }
        
        /* Cajas informativas */
        .info-box {
            background-color: """ + COLORES["azul_oscuro"] + """;
            color: """ + COLORES["blanco"] + """;
            padding: 15px;
            border-radius: 5px;
            border-left: 5px solid """ + COLORES["dorado"] + """;
            margin-bottom: 15px;
        }
        .success-box {
            background-color: """ + COLORES["verde_oscuro"] + """;
            color: """ + COLORES["blanco"] + """;
            padding: 15px;
            border-radius: 5px;
            border-left: 5px solid """ + COLORES["verde"] + """;
            margin-bottom: 15px;
        }
        .error-box {
            background-color: """ + COLORES["rojo"] + """;
            color: """ + COLORES["blanco"] + """;
            padding: 15px;
            border-radius: 5px;
            border-left: 5px solid """ + COLORES["rojo_claro"] + """;
            margin-bottom: 15px;
        }
        
        /* Botones */
        .stButton>button {
            background-color: """ + COLORES["azul"] + """;
            color: white;
            font-weight: bold;
            border: none;
            padding: 10px 20px;
            border-radius: 5px;
        }
        .stButton>button:hover {
            background-color: """ + COLORES["azul_claro"] + """;
        }
        .download-btn {
            background-color: """ + COLORES["dorado"] + """ !important;
        }
        .download-btn:hover {
            background-color: #b08a1e !important;
        }
        
        /* Tarjetas para la barra lateral */
        .sidebar-card {
            background-color: """ + COLORES["azul_oscuro"] + """;
            color: """ + COLORES["blanco"] + """;
            padding: 15px;
            border-radius: 5px;
            margin-bottom: 15px;
            border-left: 3px solid """ + COLORES["dorado"] + """;
        }
        .sidebar-card h4 {
            color: """ + COLORES["dorado"] + """;
            margin-top: 0;
            margin-bottom: 10px;
        }
        .sidebar-card ul, .sidebar-card ol {
            margin-top: 10px;
            margin-bottom: 0;
            padding-left: 20px;
        }
        .sidebar-card li {
            margin-bottom: 5px;
        }
        .sidebar-card strong {
            color: """ + COLORES["dorado"] + """;
        }
        
        /* Pie de página */
        .footer {
            text-align: center;
            margin-top: 50px;
            color: """ + COLORES["gris_medio"] + """;
            font-size: 0.8rem;
        }
    </style>
    """, unsafe_allow_html=True)

def mostrar_encabezado():
    """
    Muestra el encabezado principal de la aplicación.
    """
    st.markdown('<h1 class="main-header">DIRECCIÓN NACIONAL GUARDIA REPUBLICANA</h1>', unsafe_allow_html=True)
    st.markdown('<h2 class="sub-header">Sistema de Despliegues Operativos</h2>', unsafe_allow_html=True)

def mostrar_seccion(titulo, numero=None):
    """
    Muestra un encabezado de sección con estilo.
    
    Args:
        titulo (str): Título de la sección.
        numero (int, optional): Número de la sección. Defaults to None.
    """
    if numero:
        st.markdown(f'<div class="section-header">{numero}. {titulo}</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="section-header">{titulo}</div>', unsafe_allow_html=True)

def mostrar_info(mensaje):
    """
    Muestra un cuadro de información.
    
    Args:
        mensaje (str): Mensaje a mostrar.
    """
    st.markdown(f'<div class="info-box">{mensaje}</div>', unsafe_allow_html=True)

def mostrar_exito(mensaje):
    """
    Muestra un cuadro de éxito.
    
    Args:
        mensaje (str): Mensaje a mostrar.
    """
    st.markdown(f'<div class="success-box">{mensaje}</div>', unsafe_allow_html=True)

def mostrar_error(mensaje):
    """
    Muestra un cuadro de error.
    
    Args:
        mensaje (str): Mensaje a mostrar.
    """
    st.markdown(f'<div class="error-box">{mensaje}</div>', unsafe_allow_html=True)
