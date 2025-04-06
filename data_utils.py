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
    try:
        # Verificar que df sea un DataFrame válido
        if df is None:
            raise TypeError("El argumento df no puede ser None")
            
        if not isinstance(df, pd.DataFrame):
            raise TypeError("El argumento df debe ser un DataFrame de pandas")
            
        # Verificar que el DataFrame no esté vacío
        if df.empty:
            return df.copy(), pd.DataFrame(), []
        
        # Crear una copia explícita del DataFrame original para no modificarlo
        # Usamos reset_index para evitar problemas con índices
        df_completo = df.copy(deep=True).reset_index(drop=True)
        
        # Verificar si existen las columnas necesarias
        columnas_df = list(df_completo.columns)  # Convertir a lista para evitar problemas con índices
        tiene_tipo_operativo = 'TIPO OPERATIVO' in columnas_df
        tiene_nombre_operativo = 'NOMBRE OPERATIVO' in columnas_df
        tiene_nombre_orden = 'NOMBRE ORDEN' in columnas_df
        
        # Si existen las columnas necesarias, modificar la columna NOMBRE ORDEN para incluir ambos valores
        if tiene_tipo_operativo and tiene_nombre_operativo and tiene_nombre_orden:
            # Guardar una copia de la columna original por si acaso
            df_completo['NOMBRE_ORDEN_ORIGINAL'] = df_completo['NOMBRE ORDEN'].astype(str)
            
            # Crear una nueva columna con la combinación de TIPO OPERATIVO y NOMBRE OPERATIVO
            nueva_columna = []
            for i in range(len(df_completo)):
                fila = df_completo.iloc[i]
                tipo_op = str(fila['TIPO OPERATIVO']) if pd.notna(fila['TIPO OPERATIVO']) else ''
                nombre_op = str(fila['NOMBRE OPERATIVO']) if pd.notna(fila['NOMBRE OPERATIVO']) else ''
                nombre_orden = str(fila['NOMBRE ORDEN']) if pd.notna(fila['NOMBRE ORDEN']) else ''
                
                if tipo_op and nombre_op:
                    nueva_columna.append(f"{tipo_op} {nombre_op}")
                elif tipo_op:
                    nueva_columna.append(tipo_op)
                elif nombre_op:
                    nueva_columna.append(nombre_op)
                else:
                    nueva_columna.append(nombre_orden)
            
            # Asignar la nueva columna al DataFrame
            df_completo['NOMBRE ORDEN'] = nueva_columna
        
        # Filtrar columnas para el PDF, asegurándose de que existan en el DataFrame
        columnas_disponibles = []
        for col in COLUMNAS_PDF:
            if col in columnas_df:
                columnas_disponibles.append(col)
        
        # Crear el DataFrame filtrado con las columnas necesarias
        if columnas_disponibles:
            # Crear un nuevo DataFrame vacío
            df_filtrado = pd.DataFrame()
            
            # Copiar cada columna individualmente
            for col in columnas_disponibles:
                df_filtrado[col] = df_completo[col].copy()
        else:
            # Si no hay columnas disponibles, devolver un DataFrame vacío con las mismas filas
            df_filtrado = pd.DataFrame(index=range(len(df_completo)))
        
        return df_completo, df_filtrado, columnas_disponibles
        
    except Exception as e:
        # En caso de error, imprimir el error y devolver DataFrames vacíos
        print(f"Error en preparar_dataframe: {str(e)}")
        return pd.DataFrame(), pd.DataFrame(), []

def clasificar_datos_por_unidad(df_completo, df_filtrado):
    """
    Clasifica los datos por unidad y devuelve un diccionario con los DataFrames filtrados.
    
    Args:
        df_completo (pandas.DataFrame): DataFrame completo con todas las columnas.
        df_filtrado (pandas.DataFrame): DataFrame con solo las columnas necesarias para el PDF.
        
    Returns:
        dict: Diccionario con las unidades como claves y los DataFrames filtrados como valores.
    """
    try:
        from unidades_config import UNIDADES_ORDEN, clasificar_unidad
        
        # Verificar que ambos argumentos sean DataFrames válidos
        if df_completo is None or df_filtrado is None:
            print("Error: Uno o ambos DataFrames son None")
            return {}
            
        if not isinstance(df_completo, pd.DataFrame) or not isinstance(df_filtrado, pd.DataFrame):
            print("Error: Ambos argumentos deben ser DataFrames de pandas")
            return {}
        
        # Verificar que los DataFrames no estén vacíos
        if df_completo.empty or df_filtrado.empty:
            print("Advertencia: Uno o ambos DataFrames están vacíos")
            return {}
        
        # Verificar si la columna UNIDAD existe
        if 'UNIDAD' not in df_completo.columns:
            print("Advertencia: La columna 'UNIDAD' no existe en el DataFrame")
            return {}
        
        # Crear una copia para evitar modificar el original y resetear índices
        df_trabajo = df_completo.copy(deep=True).reset_index(drop=True)
        df_filtrado_reset = df_filtrado.copy(deep=True).reset_index(drop=True)
        
        # Asegurarse de que ambos DataFrames tengan el mismo número de filas
        if len(df_trabajo) != len(df_filtrado_reset):
            print(f"Advertencia: Los DataFrames tienen diferente número de filas: {len(df_trabajo)} vs {len(df_filtrado_reset)}")
            # Ajustar el tamaño si es necesario
            min_filas = min(len(df_trabajo), len(df_filtrado_reset))
            df_trabajo = df_trabajo.iloc[0:min_filas].copy()
            df_filtrado_reset = df_filtrado_reset.iloc[0:min_filas].copy()
        
        # Clasificar cada fila según su unidad usando método seguro
        unidades_clasificadas = []
        for i in range(len(df_trabajo)):
            try:
                unidad = df_trabajo.iloc[i]['UNIDAD']
                unidad_clasificada = clasificar_unidad(unidad)
                unidades_clasificadas.append(unidad_clasificada)
            except Exception as e:
                print(f"Error al clasificar unidad en fila {i}: {str(e)}")
                unidades_clasificadas.append(None)
        
        # Agregar la columna de unidades clasificadas
        df_trabajo['UNIDAD_CLASIFICADA'] = unidades_clasificadas
        
        # Diccionario para almacenar los DataFrames por unidad
        dfs_por_unidad = {}
        
        # Para cada unidad en el orden definido
        for unidad in UNIDADES_ORDEN:
            try:
                # Crear un nuevo DataFrame para esta unidad
                filas_unidad = []
                
                # Recorrer todas las filas y seleccionar las que corresponden a esta unidad
                for i in range(len(df_trabajo)):
                    if df_trabajo.iloc[i]['UNIDAD_CLASIFICADA'] == unidad:
                        # Obtener la fila correspondiente del DataFrame filtrado
                        fila_filtrada = df_filtrado_reset.iloc[i]
                        filas_unidad.append(fila_filtrada)
                
                # Si hay filas para esta unidad, crear un DataFrame
                if filas_unidad:
                    # Crear un nuevo DataFrame con las filas seleccionadas
                    df_unidad = pd.DataFrame(filas_unidad)
                    
                    # Agregar al diccionario si no está vacío
                    if not df_unidad.empty:
                        dfs_por_unidad[unidad] = df_unidad
            except Exception as e:
                print(f"Error al procesar la unidad {unidad}: {str(e)}")
                continue
        
        return dfs_por_unidad
        
    except Exception as e:
        print(f"Error general en clasificar_datos_por_unidad: {str(e)}")
        return {}
