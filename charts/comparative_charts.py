"""
Módulo para la generación de gráficas comparativas.
"""

import matplotlib.pyplot as plt
import numpy as np
from reportlab.lib.units import cm
from charts.config import COLOR_AZUL, COLORES_GRAFICA
from charts.utils import guardar_figura_como_imagen

def crear_grafica_comparativa(datos_categorias, titulo, etiqueta_x, etiqueta_y, ancho=15*cm, alto=10*cm):
    """
    Crea una gráfica de barras comparativa para múltiples categorías.
    
    Args:
        datos_categorias (dict): Diccionario con categorías como claves y diccionarios de subcategorías como valores.
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
    
    # Datos para el gráfico
    categorias = list(datos_categorias.keys())
    subcategorias = list(datos_categorias[categorias[0]].keys())
    
    # Número de grupos y barras
    n_categorias = len(categorias)
    n_subcategorias = len(subcategorias)
    ancho_barra = 0.8 / n_subcategorias
    
    # Posiciones de las barras
    posiciones = np.arange(n_categorias)
    
    # Crear barras para cada subcategoría
    for i, subcat in enumerate(subcategorias):
        valores = [datos_categorias[cat][subcat] for cat in categorias]
        offset = (i - n_subcategorias / 2 + 0.5) * ancho_barra
        bars = ax.bar(posiciones + offset, valores, ancho_barra * 0.9, 
                     label=subcat, color=COLORES_GRAFICA[i % len(COLORES_GRAFICA)])
        
        # Añadir valores encima de las barras
        for bar in bars:
            height = bar.get_height()
            if height > 0:  # Solo mostrar etiquetas para valores positivos
                ax.text(bar.get_x() + bar.get_width()/2., height + 0.1,
                        f'{int(height)}', ha='center', va='bottom', fontsize=8)
    
    # Configurar ejes y título
    ax.set_title(titulo, fontsize=14, fontweight='bold', pad=20, color=COLOR_AZUL)
    ax.set_xlabel(etiqueta_x, fontsize=12, labelpad=10)
    ax.set_ylabel(etiqueta_y, fontsize=12, labelpad=10)
    ax.set_xticks(posiciones)
    ax.set_xticklabels(categorias)
    
    # Añadir leyenda
    ax.legend(title="Categorías", loc='best')
    
    # Personalizar rejilla
    ax.grid(axis='y', linestyle='--', alpha=0.7)
    
    # Ajustar espaciado
    plt.tight_layout()
    
    # Guardar como imagen para ReportLab
    return guardar_figura_como_imagen(fig, ancho, alto)
