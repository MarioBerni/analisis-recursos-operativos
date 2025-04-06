"""
Módulo para el procesamiento de datos de la aplicación.
"""

import pandas as pd
from utils import leer_excel, formatear_datos, obtener_hojas_excel
from ui_styles import mostrar_error

def procesar_archivo_excel(uploaded_file, EXCEL_SHEETS):
    """
    Procesa un archivo Excel subido y valida su estructura.
    
    Args:
        uploaded_file: Archivo Excel subido.
        EXCEL_SHEETS (list): Lista de nombres de hojas esperadas.
        
    Returns:
        tuple: (df, mensaje_error) donde df es el DataFrame procesado o None si hay error,
               y mensaje_error es el mensaje de error o None si no hay error.
    """
    try:
        # Obtener las hojas disponibles en el archivo Excel
        hojas_disponibles = obtener_hojas_excel(uploaded_file)
        
        # Verificar si las hojas necesarias están presentes
        hojas_requeridas = [hoja for hoja in EXCEL_SHEETS if hoja in hojas_disponibles]
        
        if not hojas_requeridas:
            mensaje_error_hojas = (
                f"El archivo Excel no contiene las hojas esperadas. "
                f"Se esperan hojas como: {', '.join(EXCEL_SHEETS[:5])}... "
                f"Las hojas encontradas son: {', '.join(hojas_disponibles[:5])}..."
            )
            return None, mensaje_error_hojas
        
        # Leer el archivo Excel
        try:
            df = leer_excel(uploaded_file)
            
            # Formatear los datos
            df = formatear_datos(df)
            
            return df, None
            
        except Exception as e:
            mensaje_error = f"Error al procesar el archivo: {str(e)}"
            return None, mensaje_error
            
    except Exception as e:
        mensaje_error = f"Error al procesar el archivo: {str(e)}"
        return None, mensaje_error

def generar_parametros_pdf(organizar_por_unidad, reporte_cumplimiento, mes_seleccionado=None, año_seleccionado=None):
    """
    Genera los parámetros para la generación del PDF.
    
    Args:
        organizar_por_unidad (bool): Si se debe organizar por unidad.
        reporte_cumplimiento (bool): Si se debe generar un reporte de cumplimiento.
        mes_seleccionado (str, optional): Mes seleccionado. Defaults to None.
        año_seleccionado (int, optional): Año seleccionado. Defaults to None.
        
    Returns:
        dict: Diccionario con los parámetros para la generación del PDF.
    """
    params = {
        "organizar_por_unidad": organizar_por_unidad,
        "reporte_cumplimiento": reporte_cumplimiento
    }
    
    # Si es un reporte de cumplimiento, añadir mes y año
    if reporte_cumplimiento and mes_seleccionado and año_seleccionado:
        params["mes"] = mes_seleccionado
        params["año"] = año_seleccionado
    
    return params
