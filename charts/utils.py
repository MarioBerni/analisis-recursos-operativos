"""
Utilidades comunes para la generación de gráficas.
"""

import io
import matplotlib.pyplot as plt
from reportlab.platypus import Image

def guardar_figura_como_imagen(fig, ancho, alto):
    """
    Guarda una figura de matplotlib como una imagen para ReportLab.
    
    Args:
        fig (matplotlib.figure.Figure): Figura de matplotlib.
        ancho (float): Ancho de la imagen en cm.
        alto (float): Alto de la imagen en cm.
        
    Returns:
        Image: Objeto Image de ReportLab con la gráfica.
    """
    # Convertir a imagen para ReportLab
    img_data = io.BytesIO()
    plt.savefig(img_data, format='png', bbox_inches='tight')
    img_data.seek(0)
    plt.close(fig)
    
    # Crear objeto Image de ReportLab
    img = Image(img_data, width=ancho, height=alto)
    
    return img
