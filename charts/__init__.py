"""
Paquete para la generación de gráficas para los reportes.
"""

from charts.config import COLOR_DORADO, COLOR_AZUL, COLORES_GRAFICA
from charts.bar_charts import crear_grafica_barras
from charts.pie_charts import crear_grafica_pastel
from charts.line_charts import crear_grafica_lineas_tiempo
from charts.comparative_charts import crear_grafica_comparativa

__all__ = [
    'COLOR_DORADO', 
    'COLOR_AZUL', 
    'COLORES_GRAFICA',
    'crear_grafica_barras',
    'crear_grafica_pastel',
    'crear_grafica_lineas_tiempo',
    'crear_grafica_comparativa'
]
