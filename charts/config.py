"""
Configuración para la generación de gráficas.
"""

import matplotlib.pyplot as plt
import matplotlib

# Configurar matplotlib para usar un estilo adecuado para los reportes
matplotlib.use('Agg')  # Necesario para generar gráficos sin interfaz gráfica
plt.style.use('seaborn-v0_8-darkgrid')

# Colores institucionales
COLOR_DORADO = '#CCAA33'
COLOR_AZUL = '#003366'
COLORES_GRAFICA = [COLOR_DORADO, COLOR_AZUL, '#669933', '#993366', '#336699', '#996633']
