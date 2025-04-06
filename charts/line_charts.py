"""
Módulo para la generación de gráficas de líneas temporales.
"""

import matplotlib.pyplot as plt
from reportlab.lib.units import cm
from charts.config import COLOR_DORADO, COLOR_AZUL
from charts.utils import guardar_figura_como_imagen

def crear_grafica_lineas_tiempo(datos_por_fecha, titulo, etiqueta_x, etiqueta_y, ancho=15*cm, alto=10*cm):
    """
    Crea una gráfica de líneas para mostrar evolución temporal.
    
    Args:
        datos_por_fecha (dict): Diccionario con fechas como claves y valores como valores.
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
    fechas = list(datos_por_fecha.keys())
    valores = list(datos_por_fecha.values())
    
    # Crear gráfico de líneas
    ax.plot(fechas, valores, marker='o', linestyle='-', linewidth=2, 
            color=COLOR_AZUL, markersize=8, markerfacecolor=COLOR_DORADO)
    
    # Añadir valores sobre los puntos
    for i, valor in enumerate(valores):
        ax.text(i, valor + max(valores)*0.02, f'{valor}', ha='center', va='bottom', 
                fontweight='bold', color=COLOR_AZUL)
    
    # Configurar ejes y título
    ax.set_title(titulo, fontsize=14, fontweight='bold', pad=20, color=COLOR_AZUL)
    ax.set_xlabel(etiqueta_x, fontsize=12, labelpad=10)
    ax.set_ylabel(etiqueta_y, fontsize=12, labelpad=10)
    
    # Personalizar rejilla
    ax.grid(True, linestyle='--', alpha=0.7)
    
    # Rotar etiquetas del eje X si son fechas
    plt.xticks(rotation=45)
    
    # Ajustar espaciado
    plt.tight_layout()
    
    # Guardar como imagen para ReportLab
    return guardar_figura_como_imagen(fig, ancho, alto)
