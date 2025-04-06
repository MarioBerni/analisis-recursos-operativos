"""
Configuración de unidades para la organización de tablas en el PDF.
"""

# Mapeo de unidades a sus nombres completos para los títulos de las tablas
UNIDADES_NOMBRES = {
    "DIRECCIÓN I": "Dirección I - Zona Metropolitana",
    "DIRECCIÓN II": "Dirección II - Unidades Especiales",
    "GEO": "GEO - Grupo Especial de Operaciones",
    "REGIONAL ESTE": "Dirección III - Regional Este",
    "REGIONAL NORTE": "Dirección III - Regional Norte",
    "OTRAS": "Otras Unidades de apoyo"
}

# Orden de las unidades para mostrar en el PDF
UNIDADES_ORDEN = [
    "DIRECCIÓN I",
    "DIRECCIÓN II",
    "GEO",
    "REGIONAL ESTE",
    "REGIONAL NORTE",
    "OTRAS"
]

# Función para obtener el nombre completo de una unidad
def obtener_nombre_unidad(unidad):
    """
    Obtiene el nombre completo de una unidad para mostrar en el título de la tabla.
    
    Args:
        unidad: Código de la unidad
        
    Returns:
        str: Nombre completo de la unidad
    """
    # Si la unidad está en el mapeo, devolver su nombre completo
    if unidad in UNIDADES_NOMBRES:
        return UNIDADES_NOMBRES[unidad]
    
    # Si no está en el mapeo, considerarla como "OTRAS"
    return UNIDADES_NOMBRES["OTRAS"]

# Función para clasificar una unidad
def clasificar_unidad(unidad):
    """
    Clasifica una unidad según el mapeo definido.
    
    Args:
        unidad: Nombre de la unidad a clasificar
        
    Returns:
        str: Categoría de la unidad (una de las definidas en UNIDADES_ORDEN)
    """
    # Si la unidad está en el mapeo, devolverla
    if unidad in UNIDADES_NOMBRES:
        return unidad
    
    # Si no está en el mapeo, considerarla como "OTRAS"
    return "OTRAS"
