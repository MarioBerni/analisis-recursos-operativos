"""
Utilidades para la preparación y manipulación de datos para la generación de PDFs.
"""

import pandas as pd
from pdf_config import COLUMNAS_PDF

def preparar_dataframe(df):
    """
    Prepara el DataFrame para la generación del PDF, combinando las columnas TIPO OPERATIVO y NOMBRE OPERATIVO.
    
    Args:
        df (pandas.DataFrame): DataFrame original con los datos de despliegues operativos.
        
    Returns:
        tuple: Tupla con (df_completo, df_filtrado, columnas_disponibles)
            - df_completo: DataFrame completo con todas las columnas
            - df_filtrado: DataFrame con solo las columnas necesarias para el PDF
            - columnas_disponibles: Lista de columnas disponibles para el PDF
    """
    # Crear una copia del DataFrame original para no modificarlo
    df_completo = df.copy()
    
    # Verificar si existen las columnas necesarias
    tiene_tipo_operativo = 'TIPO OPERATIVO' in df_completo.columns
    tiene_nombre_operativo = 'NOMBRE OPERATIVO' in df_completo.columns
    
    # Si existen las columnas necesarias, modificar la columna NOMBRE ORDEN para incluir ambos valores
    if tiene_tipo_operativo and tiene_nombre_operativo:
        # Guardar una copia de la columna original por si acaso
        df_completo['NOMBRE_ORDEN_ORIGINAL'] = df_completo['NOMBRE ORDEN']
        
        # Modificar la columna NOMBRE ORDEN para incluir TIPO OPERATIVO y NOMBRE OPERATIVO
        df_completo['NOMBRE ORDEN'] = df_completo.apply(
            lambda row: f"{row['TIPO OPERATIVO']} {row['NOMBRE OPERATIVO']}" 
            if pd.notna(row['TIPO OPERATIVO']) and pd.notna(row['NOMBRE OPERATIVO']) 
            else (row['TIPO OPERATIVO'] if pd.notna(row['TIPO OPERATIVO']) else 
                  (row['NOMBRE OPERATIVO'] if pd.notna(row['NOMBRE OPERATIVO']) else row['NOMBRE ORDEN'])),
            axis=1
        )
    
    # Filtrar columnas para el PDF, asegurándose de que existan en el DataFrame
    columnas_disponibles = [col for col in COLUMNAS_PDF if col in df.columns]
    
    # Crear el DataFrame filtrado con las columnas necesarias
    df_filtrado = df_completo[columnas_disponibles].copy()
    
    return df_completo, df_filtrado, columnas_disponibles

def clasificar_datos_por_unidad(df_completo, df_filtrado):
    """
    Clasifica los datos por unidad y devuelve un diccionario con los DataFrames filtrados.
    
    Args:
        df_completo (pandas.DataFrame): DataFrame completo con todas las columnas.
        df_filtrado (pandas.DataFrame): DataFrame con solo las columnas necesarias para el PDF.
        
    Returns:
        dict: Diccionario con las unidades como claves y los DataFrames filtrados como valores.
    """
    from unidades_config import UNIDADES_ORDEN, clasificar_unidad
    
    # Verificar si la columna UNIDAD existe
    if 'UNIDAD' not in df_completo.columns:
        return {}
    
    # Clasificar cada fila según su unidad
    df_completo['UNIDAD_CLASIFICADA'] = df_completo['UNIDAD'].apply(clasificar_unidad)
    
    # Diccionario para almacenar los DataFrames por unidad
    dfs_por_unidad = {}
    
    # Para cada unidad en el orden definido
    for unidad in UNIDADES_ORDEN:
        # Filtrar el DataFrame para obtener solo las filas de esta unidad
        filas_unidad = df_completo['UNIDAD_CLASIFICADA'] == unidad
        
        # Si hay datos para esta unidad, crear un DataFrame filtrado
        if filas_unidad.any():
            # Obtener los índices de las filas que corresponden a esta unidad
            indices_unidad = df_completo[filas_unidad].index
            
            # Filtrar el DataFrame con las columnas para el PDF usando los mismos índices
            df_unidad = df_filtrado.loc[indices_unidad].copy()
            
            # Si hay datos para esta unidad, agregarlo al diccionario
            if not df_unidad.empty:
                dfs_por_unidad[unidad] = df_unidad
    
    return dfs_por_unidad
