"""
Módulo para la generación de gráficas de barras.
"""

import matplotlib.pyplot as plt
from reportlab.lib.units import cm
from charts.config import COLOR_DORADO, COLOR_AZUL
from charts.utils import guardar_figura_como_imagen

def crear_grafica_barras(datos, titulo, etiqueta_x, etiqueta_y, ancho=15*cm, alto=10*cm):
    """
    Crea una gráfica de barras a partir de un diccionario de datos.
    
    Args:
        datos (dict): Diccionario con las categorías como claves y los valores como valores.
        titulo (str): Título de la gráfica.
        etiqueta_x (str): Etiqueta para el eje X.
        etiqueta_y (str): Etiqueta para el eje Y.
        ancho (float): Ancho de la imagen en cm.
        alto (float): Alto de la imagen en cm.
        
    Returns:
        Image: Objeto Image de ReportLab con la gráfica.
    """
    # Crear figura
    fig, ax = plt.subplots(figsize=(ancho/cm*0.4, alto/cm*0.4), dpi=100)
    
    # Crear gráfica de barras
    categorias = list(datos.keys())
    valores = list(datos.values())
    
    # Crear barras con colores institucionales
    bars = ax.bar(categorias, valores, color=COLOR_DORADO, edgecolor=COLOR_AZUL, linewidth=1.5)
    
    # Añadir valores encima de las barras
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height + 0.1,
                f'{int(height)}', ha='center', va='bottom', fontweight='bold')
    
    # Configurar ejes y título
    ax.set_title(titulo, fontsize=14, fontweight='bold', pad=20, color=COLOR_AZUL)
    ax.set_xlabel(etiqueta_x, fontsize=12, labelpad=10)
    ax.set_ylabel(etiqueta_y, fontsize=12, labelpad=10)
    
    # Personalizar rejilla
    ax.grid(axis='y', linestyle='--', alpha=0.7)
    
    # Ajustar espaciado
    plt.tight_layout()
    
    # Guardar como imagen para ReportLab
    return guardar_figura_como_imagen(fig, ancho, alto)
