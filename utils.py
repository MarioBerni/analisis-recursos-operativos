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
        # Obtener todas las hojas disponibles
        xls = pd.ExcelFile(archivo)
        hojas_disponibles = xls.sheet_names
        
        # Si no se especifica hoja, usar la hoja 'OPERATIVOS' o la primera disponible
        if hoja is None:
            if 'OPERATIVOS' in hojas_disponibles:
                hoja = 'OPERATIVOS'
            else:
                hoja = hojas_disponibles[0]  # Primera hoja disponible
        
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
        
        # Si es una hoja de día (01-31), añadir una columna con la fecha
        if hoja in [f"{i:02d}" for i in range(1, 32)]:
            # Extraer el día del nombre de la hoja
            dia = int(hoja)
            # Añadir columna de fecha (el mes y año se deben proporcionar externamente)
            df['DIA'] = dia
        
        # Formatear los datos según los tipos esperados
        df = formatear_datos(df)
        
        # Para hojas diarias, no validamos estrictamente las columnas
        if hoja in [f"{i:02d}" for i in range(1, 32)]:
            return df, True, ""
        else:
            # Validar el DataFrame para la hoja OPERATIVOS
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
        # Verificar que el archivo no sea None
        if archivo is None:
            return [], False, "No se ha seleccionado ningún archivo"
            
        # Intentar leer el archivo Excel
        try:
            xls = pd.ExcelFile(archivo)
            hojas_disponibles = xls.sheet_names
            
            # Verificar que haya al menos una hoja
            if not hojas_disponibles:
                return [], False, "El archivo Excel no contiene hojas"
                
            return hojas_disponibles, True, ""
            
        except Exception as e:
            return [], False, f"Error al leer las hojas del archivo Excel: {str(e)}"
            
    except Exception as e:
        return [], False, f"Error inesperado al procesar el archivo: {str(e)}"

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
    
    # Convertir columnas numéricas a sus tipos correspondientes
    from config import NUMERIC_COLUMNS, MULTI_VALUE_COLUMNS
    
    # Procesar columnas numéricas
    for col in NUMERIC_COLUMNS:
        if col in df_formateado.columns:
            # Las columnas de hora se mantienen como string para preservar el formato
            if col in ["HORA INICIO", "HORA FIN"]:
                continue
            
            # La columna PORCENTAJE se maneja como decimal
            if col == "PORCENTAJE":
                df_formateado[col] = pd.to_numeric(df_formateado[col], errors='coerce').fillna(0)
            # El resto de columnas numéricas se convierten a enteros
            else:
                df_formateado[col] = pd.to_numeric(df_formateado[col], errors='coerce').fillna(0).astype(int)
    
    # Procesar columnas con múltiples valores
    for col in MULTI_VALUE_COLUMNS:
        if col in df_formateado.columns:
            # Asegurar que los valores sean strings antes de cualquier procesamiento
            df_formateado[col] = df_formateado[col].astype(str)
            # Limpiar valores vacíos o 'nan'
            df_formateado[col] = df_formateado[col].replace('nan', '').replace('None', '')
    
    return df_formateado
