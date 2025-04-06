"""
Módulo para la generación de reportes de cumplimiento de servicios.
Este archivo sirve como punto de entrada para la funcionalidad de reportes,
importando y exponiendo la función principal desde la estructura modularizada.
"""

# Importar la función principal desde el módulo modularizado
from report_services.core import crear_reporte_cumplimiento

# Exportar solo la función principal para mantener la compatibilidad con el código existente
__all__ = ['crear_reporte_cumplimiento']