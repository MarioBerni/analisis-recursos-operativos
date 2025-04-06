"""
Módulo para la generación de gráficas de pastel.
"""

import matplotlib.pyplot as plt
from reportlab.lib.units import cm
from charts.config import COLOR_AZUL, COLORES_GRAFICA
from charts.utils import guardar_figura_como_imagen

def crear_grafica_pastel(datos, titulo, ancho=15*cm, alto=10*cm):
    """
    Crea una gráfica de pastel a partir de un diccionario de datos.
    
    Args:
        datos (dict): Diccionario con las categorías como claves y los valores como valores.
        titulo (str): Título de la gráfica.
        ancho (float): Ancho de la imagen en cm.
        alto (float): Alto de la imagen en cm.
        
    Returns:
        Image: Objeto Image de ReportLab con la gráfica.
    """
    # Crear figura
    fig, ax = plt.subplots(figsize=(ancho/cm*0.4, alto/cm*0.4), dpi=100)
    
    # Datos para el gráfico
    categorias = list(datos.keys())
    valores = list(datos.values())
    
    # Calcular porcentajes
    total = sum(valores)
    porcentajes = [valor/total*100 for valor in valores]
    
    # Crear gráfico de pastel
    wedges, texts, autotexts = ax.pie(
        valores, 
        labels=categorias,
        autopct='%1.1f%%',
        startangle=90,
        colors=COLORES_GRAFICA[:len(categorias)],
        wedgeprops={'edgecolor': 'white', 'linewidth': 1.5},
        textprops={'fontsize': 10, 'fontweight': 'bold'}
    )
    
    # Personalizar textos
    for autotext in autotexts:
        autotext.set_fontsize(9)
        autotext.set_fontweight('bold')
        autotext.set_color('white')
    
    # Añadir título
    ax.set_title(titulo, fontsize=14, fontweight='bold', pad=20, color=COLOR_AZUL)
    
    # Añadir leyenda con valores absolutos
    leyendas = [f'{cat}: {val} ({pct:.1f}%)' for cat, val, pct in zip(categorias, valores, porcentajes)]
    ax.legend(leyendas, loc='best', fontsize=9)
    
    # Ajustar espaciado
    plt.tight_layout()
    
    # Guardar como imagen para ReportLab
    return guardar_figura_como_imagen(fig, ancho, alto)
