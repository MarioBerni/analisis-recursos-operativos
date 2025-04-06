"""
Utilidades para la generación de elementos de tabla en PDFs.
"""

import pandas as pd
from reportlab.platypus import Paragraph, Spacer, Table, TableStyle
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle

from image_utils import cargar_imagen_svg
from pdf_table_utils import definir_anchos_columnas, ICONOS_COLUMNAS
from unidades_config import obtener_nombre_unidad

# Constantes para cabeceras personalizadas
CABECERAS_PERSONALIZADAS = {
    'NOMBRE ORDEN': 'SERVICIO',
    'CANTIDAD': 'EFECTIVOS',
    'HORARIO': 'HORA',
    'HORA INICIO': 'INICIO',
    'HORA FIN': 'FIN',
    # Agregar más cabeceras personalizadas según sea necesario
}

def generar_titulo_unidad(unidad):
    """
    Genera un título para la sección de una unidad específica.
    
    Args:
        unidad (str): Nombre de la unidad.
        
    Returns:
        Paragraph: Título formateado para la unidad.
    """
    nombre_unidad = obtener_nombre_unidad(unidad)
    titulo_estilo = ParagraphStyle(
        'TituloUnidad',
        fontName='Helvetica-Bold',
        fontSize=12,
        textColor=colors.navy,
        spaceAfter=0.5*cm,
        alignment=1,  # 1 = centro (0=izquierda, 2=derecha)
        spaceBefore=2.0*cm,  # Espacio aumentado antes del título
        keepWithNext=True  # Mantener con el siguiente elemento (la tabla)
    )
    return Paragraph(f"<b>{nombre_unidad}</b>", titulo_estilo)

def generar_encabezados_tabla(columnas_disponibles):
    """
    Genera los encabezados de la tabla, incluyendo imágenes para las columnas que lo requieran.
    
    Args:
        columnas_disponibles (list): Lista de nombres de columnas disponibles.
        
    Returns:
        tuple: Tupla con (cabeceras, columnas_con_imagenes)
            - cabeceras: Lista de elementos de encabezado (texto o imágenes)
            - columnas_con_imagenes: Lista de índices de columnas que tienen imágenes
    """
    cabeceras = []
    columnas_con_imagenes = []
    
    for i, col in enumerate(columnas_disponibles):
        # Verificar si la columna tiene un icono asociado
        if col in ICONOS_COLUMNAS:
            img = cargar_imagen_svg(ICONOS_COLUMNAS[col])
            if img:
                cabeceras.append(img)
                # Registrar que esta columna tiene imagen
                columnas_con_imagenes.append(i)
                continue
        
        # Si no hay imagen o no se pudo cargar, usar texto
        # Usar cabecera personalizada si existe, de lo contrario usar el nombre de la columna
        texto_cabecera = CABECERAS_PERSONALIZADAS.get(col, col)
        cabeceras.append(texto_cabecera)
    
    return cabeceras, columnas_con_imagenes

def generar_datos_tabla(df_unidad, columnas_disponibles, estilos):
    """
    Genera los datos para la tabla a partir del DataFrame filtrado por unidad.
    
    Args:
        df_unidad (pandas.DataFrame): DataFrame filtrado para una unidad específica.
        columnas_disponibles (list): Lista de nombres de columnas disponibles.
        estilos (dict): Diccionario con los estilos para la tabla.
        
    Returns:
        list: Lista de filas con los datos formateados para la tabla.
    """
    datos = []
    
    # Procesar cada fila del DataFrame
    for _, fila in df_unidad.iterrows():
        fila_datos = []
        for i, col in enumerate(columnas_disponibles):
            # Simplemente usar el valor de la columna (ya combinado si corresponde)
            valor = str(fila[col]) if pd.notna(fila[col]) else ""
            
            # Asegurar que todas las filas tengan al menos dos líneas de altura
            # Verificar si el texto ya ocupa más de una línea
            # Consideramos que un texto ocupa más de una línea si:
            # 1. Contiene un salto de línea explícito (<br/> o \n)
            # 2. Es un texto largo (más de 20 caracteres) que probablemente se envuelve
            # 3. Contiene caracteres que indican que es un texto con formato especial
            if "<br/>" not in valor and "\n" not in valor and len(valor) <= 20 and " Y " not in valor.upper():
                # Para columnas numéricas (columnas > 0), centrar verticalmente añadiendo espacios arriba y abajo
                if i > 0:
                    valor = "<para autoLeading='max'><br/>&nbsp;" + valor + "<br/>&nbsp;</para>"
                else:
                    valor = valor + "<br/>&nbsp;"
            else:
                # Para columnas numéricas existentes, asegurar que estén centradas verticalmente
                if i > 0 and valor.strip() and "<para" not in valor:
                    valor = "<para autoLeading='max'>" + valor + "</para>"
            
            # Usar estilo diferente para la primera columna
            estilo = estilos['first_col'] if i == 0 else estilos['data']
            
            # Crear un Paragraph con el estilo adecuado
            celda = Paragraph(valor, estilo)
            fila_datos.append(celda)
        
        datos.append(fila_datos)
    
    return datos

def crear_tabla_por_unidad(unidad, df_unidad, columnas_disponibles, estilos):
    """
    Crea una tabla completa para una unidad específica, incluyendo título y datos.
    
    Args:
        unidad (str): Nombre de la unidad.
        df_unidad (pandas.DataFrame): DataFrame filtrado para la unidad.
        columnas_disponibles (list): Lista de columnas disponibles.
        estilos (dict): Diccionario con los estilos para la tabla.
        
    Returns:
        list: Lista de elementos para el PDF (título y tabla).
    """
    from table_styles import crear_estilo_tabla_detallado, aplicar_colores_alternos
    from reportlab.platypus import KeepTogether
    
    # Crear una lista para los elementos que deben mantenerse juntos
    elementos_juntos = []
    
    # Agregar título de la unidad
    elementos_juntos.append(generar_titulo_unidad(unidad))
    
    # Generar encabezados con imágenes si corresponde
    cabeceras, columnas_con_imagenes = generar_encabezados_tabla(columnas_disponibles)
    
    # Generar datos de la tabla
    datos_tabla = [cabeceras]
    filas_datos = generar_datos_tabla(df_unidad, columnas_disponibles, estilos)
    datos_tabla.extend(filas_datos)
    
    # Definir anchos de columnas
    anchos_columnas = definir_anchos_columnas(len(columnas_disponibles))
    
    # Crear la tabla con los datos
    tabla = Table(datos_tabla, colWidths=anchos_columnas, repeatRows=1)  # Repetir la fila de encabezado en cada página
    
    # Aplicar estilos a la tabla usando la función crear_estilo_tabla_detallado
    estilo_tabla = crear_estilo_tabla_detallado(columnas_con_imagenes, estilos)
    
    # Aplicar el efecto cebra (colores alternos) a las filas
    estilo_tabla = aplicar_colores_alternos(estilo_tabla, len(filas_datos))
    
    tabla.setStyle(TableStyle(estilo_tabla))
    
    # Agregar la tabla a los elementos que deben mantenerse juntos
    elementos_juntos.append(tabla)
    
    # Usar KeepTogether para asegurar que el título y al menos la primera fila de la tabla
    # permanezcan juntos en la misma página
    elementos = [KeepTogether(elementos_juntos)]
    
    # Agregar espacio después del grupo
    elementos.append(Spacer(1, 0.5*cm))
    
    return elementos

def crear_tabla_general(df_filtrado, columnas_disponibles, estilos):
    """
    Crea una tabla general con todos los datos.
    
    Args:
        df_filtrado (pandas.DataFrame): DataFrame filtrado con las columnas para el PDF.
        columnas_disponibles (list): Lista de columnas disponibles.
        estilos (dict): Diccionario con los estilos para la tabla.
        
    Returns:
        list: Lista de elementos para el PDF (título y tabla).
    """
    from table_styles import crear_estilo_tabla_detallado, aplicar_colores_alternos
    from reportlab.platypus import KeepTogether
    
    # Crear una lista para los elementos que deben mantenerse juntos
    elementos_juntos = []
    
    # Crear un título general para la tabla
    titulo_estilo = ParagraphStyle(
        'TituloGeneral',
        fontName='Helvetica-Bold',
        fontSize=14,
        textColor=colors.navy,
        spaceAfter=0.5*cm,
        alignment=1,  # 1 = centro
        spaceBefore=2.0*cm,  # Espacio aumentado antes del título
        keepWithNext=True  # Mantener con el siguiente elemento (la tabla)
    )
    elementos_juntos.append(Paragraph("<b>Despliegues Operativos</b>", titulo_estilo))
    
    # Generar encabezados con imágenes si corresponde
    cabeceras, columnas_con_imagenes = generar_encabezados_tabla(columnas_disponibles)
    
    # Generar datos de la tabla
    datos_tabla = [cabeceras]
    filas_datos = generar_datos_tabla(df_filtrado, columnas_disponibles, estilos)
    datos_tabla.extend(filas_datos)
    
    # Definir anchos de columnas
    anchos_columnas = definir_anchos_columnas(len(columnas_disponibles))
    
    # Crear la tabla con los datos
    tabla = Table(datos_tabla, colWidths=anchos_columnas, repeatRows=1)  # Repetir la fila de encabezado en cada página
    
    # Aplicar estilos a la tabla usando la función crear_estilo_tabla_detallado
    estilo_tabla = crear_estilo_tabla_detallado(columnas_con_imagenes, estilos)
    
    # Aplicar el efecto cebra (colores alternos) a las filas
    estilo_tabla = aplicar_colores_alternos(estilo_tabla, len(filas_datos))
    
    tabla.setStyle(TableStyle(estilo_tabla))
    
    # Agregar la tabla a los elementos que deben mantenerse juntos
    elementos_juntos.append(tabla)
    
    # Usar KeepTogether para asegurar que el título y al menos la primera fila de la tabla
    # permanezcan juntos en la misma página
    elementos = [KeepTogether(elementos_juntos)]
    
    return elementos
