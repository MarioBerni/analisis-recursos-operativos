"""
Funciones de utilidad para la aplicación de conversión de Excel a PDF.
"""

import pandas as pd
import io
from config import EXPECTED_COLUMNS, EXCEL_SHEETS

def normalizar_texto(texto):
    """
    Normaliza un texto para comparaciones (quita espacios, acentos, etc.)
    
    Args:
        texto: Texto a normalizar
        
    Returns:
        str: Texto normalizado
    """
    if not isinstance(texto, str):
        return str(texto)
    
    return texto.strip().replace('Ó', 'O').replace('ó', 'o').replace('Á', 'A').replace('á', 'a').upper()

def validar_csv(df):
    """
    Valida que el DataFrame tenga las columnas esperadas.
    
    Args:
        df: DataFrame de pandas con los datos a validar
        
    Returns:
        tuple: (bool, str) - (es_valido, mensaje_error)
    """
    # Normalizar nombres de columnas para comparación
    columnas_normalizadas = {normalizar_texto(col): col for col in df.columns}
    expected_normalizadas = [normalizar_texto(col) for col in EXPECTED_COLUMNS]
    
    # Verificar que todas las columnas esperadas estén presentes (comparando versiones normalizadas)
    columnas_faltantes = []
    for col_esperada in expected_normalizadas:
        if col_esperada not in columnas_normalizadas:
            # Buscar la versión original para mostrar en el mensaje de error
            idx = expected_normalizadas.index(col_esperada)
            columnas_faltantes.append(EXPECTED_COLUMNS[idx])
    
    if columnas_faltantes:
        return False, f"Faltan las siguientes columnas: {', '.join(columnas_faltantes)}"
    
    return True, ""

def detectar_separador(archivo):
    """
    Detecta el separador utilizado en el archivo CSV.
    
    Args:
        archivo: Archivo CSV cargado por el usuario
        
    Returns:
        str: Separador detectado (coma o tabulación)
    """
    # Guardar la posición actual del archivo
    pos = archivo.tell()
    
    # Leer las primeras líneas del archivo
    contenido = archivo.read(1024).decode('utf-8')
    
    # Restaurar la posición del archivo
    archivo.seek(pos)
    
    # Contar ocurrencias de separadores comunes
    comas = contenido.count(',')
    tabs = contenido.count('\t')
    
    # Determinar el separador más probable
    if comas > tabs:
        return ','
    else:
        return '\t'

def leer_csv(archivo, separador=None):
    """
    Lee un archivo CSV y lo convierte en un DataFrame de pandas.
    
    Args:
        archivo: Archivo CSV cargado por el usuario
        separador: Separador de columnas en el CSV (si es None, se detecta automáticamente)
        
    Returns:
        tuple: (DataFrame, bool, str) - (datos, es_valido, mensaje_error)
    """
    try:
        # Detectar separador si no se especifica
        if separador is None:
            separador = detectar_separador(archivo)
        
        # Leer el archivo CSV
        df = pd.read_csv(archivo, sep=separador)
        
        # Renombrar columnas para que coincidan exactamente con las esperadas
        # Esto ayuda a manejar diferencias en espacios y acentos
        columnas_actuales = df.columns
        columnas_normalizadas = {col: normalizar_texto(col) for col in columnas_actuales}
        expected_normalizadas = {col: normalizar_texto(col) for col in EXPECTED_COLUMNS}
        
        # Crear mapeo de nombres actuales a nombres esperados
        mapeo_columnas = {}
        for col_actual, col_norm in columnas_normalizadas.items():
            for col_esperada, esp_norm in expected_normalizadas.items():
                if col_norm == esp_norm:
                    mapeo_columnas[col_actual] = col_esperada
                    break
        
        # Renombrar columnas si es necesario
        if mapeo_columnas:
            df = df.rename(columns=mapeo_columnas)
        
        # Validar el DataFrame
        es_valido, mensaje_error = validar_csv(df)
        
        return df, es_valido, mensaje_error
    
    except Exception as e:
        return None, False, f"Error al procesar el archivo: {str(e)}"


def leer_excel(archivo, hoja=None):
    """
    Lee un archivo Excel y lo convierte en un DataFrame de pandas.
    
    Args:
        archivo: Archivo Excel cargado por el usuario
        hoja: Nombre de la hoja a leer (si es None, se lee la primera hoja)
        
    Returns:
        tuple: (DataFrame, bool, str) - (datos, es_valido, mensaje_error)
    """
    try:
        # Si no se especifica hoja, usar la primera hoja disponible
        if hoja is None:
            # Verificar si la hoja 'OPERATIVOS' existe
            xls = pd.ExcelFile(archivo)
            hojas_disponibles = xls.sheet_names
            
            if 'OPERATIVOS' in hojas_disponibles:
                hoja = 'OPERATIVOS'
            else:
                hoja = hojas_disponibles[0]  # Primera hoja disponible
                
            # Informar si no se encontró alguna hoja esperada
            hojas_faltantes = [h for h in EXCEL_SHEETS.keys() if h not in hojas_disponibles]
            if hojas_faltantes:
                return None, False, f"No se encontraron las siguientes hojas esperadas: {', '.join(hojas_faltantes)}"
        
        # Leer la hoja especificada
        df = pd.read_excel(archivo, sheet_name=hoja)
        
        # Renombrar columnas para que coincidan exactamente con las esperadas
        # Esto ayuda a manejar diferencias en espacios y acentos
        columnas_actuales = df.columns
        columnas_normalizadas = {col: normalizar_texto(col) for col in columnas_actuales}
        expected_normalizadas = {col: normalizar_texto(col) for col in EXPECTED_COLUMNS}
        
        # Crear mapeo de nombres actuales a nombres esperados
        mapeo_columnas = {}
        for col_actual, col_norm in columnas_normalizadas.items():
            for col_esperada, esp_norm in expected_normalizadas.items():
                if col_norm == esp_norm:
                    mapeo_columnas[col_actual] = col_esperada
                    break
        
        # Renombrar columnas si es necesario
        if mapeo_columnas:
            df = df.rename(columns=mapeo_columnas)
        
        # Validar el DataFrame
        es_valido, mensaje_error = validar_csv(df)
        
        return df, es_valido, mensaje_error
    
    except Exception as e:
        return None, False, f"Error al procesar el archivo Excel: {str(e)}"


def obtener_hojas_excel(archivo):
    """
    Obtiene la lista de hojas disponibles en un archivo Excel.
    
    Args:
        archivo: Archivo Excel cargado por el usuario
        
    Returns:
        tuple: (list, bool, str) - (lista_hojas, es_valido, mensaje_error)
    """
    try:
        xls = pd.ExcelFile(archivo)
        hojas_disponibles = xls.sheet_names
        return hojas_disponibles, True, ""
    except Exception as e:
        return [], False, f"Error al leer las hojas del archivo Excel: {str(e)}"

def formatear_datos(df):
    """
    Realiza formateo y limpieza de datos si es necesario.
    
    Args:
        df: DataFrame de pandas con los datos a formatear
        
    Returns:
        DataFrame: DataFrame formateado
    """
    # Copia para no modificar el original
    df_formateado = df.copy()
    
    # Asegurar que todas las columnas esperadas existan (incluso si están vacías)
    for col in EXPECTED_COLUMNS:
        if col not in df_formateado.columns:
            df_formateado[col] = ""
    
    # Convertir columnas numéricas a enteros donde corresponda
    columnas_numericas = ["MOVILES", "MOTOS", "HIPO", "PP.SS EN MOVIL", "PP.SS PIE TIERRA", 
                        "CHOQUE APOSTADO", "CHOQUE ALERTA", "GEO APOSTADO", "GEO ALERTA", "PP.SS TOTAL"]
    
    for col in columnas_numericas:
        if col in df_formateado.columns:
            df_formateado[col] = pd.to_numeric(df_formateado[col], errors='coerce').fillna(0).astype(int)
    
    return df_formateado
