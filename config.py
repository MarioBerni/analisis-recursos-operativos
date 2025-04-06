"""
Configuraciones y constantes para la aplicación de conversión de Excel a PDF.
"""

# Configuración de la aplicación
APP_TITLE = "Conversor de Despliegues Operativos Excel a PDF"
APP_ICON = "📊"
APP_DESCRIPTION = "Esta aplicación permite cargar un archivo Excel con información de despliegues operativos y convertirlo a PDF."

# Configuración del PDF
PDF_FILENAME = "despliegues_operativos.pdf"
PDF_TITLE = "Informe de Despliegues Operativos"
PDF_HEADER = "INFORME DE DESPLIEGUES OPERATIVOS"
PDF_FOOTER = "Estado Mayor Policial - Página %d"

# Información de columnas esperadas
EXPECTED_COLUMNS = [
    "UNIDAD",
    "TIPO ORDEN",
    "NUMERO ORDEN",
    "NOMBRE ORDEN",
    "NOMBRE OPERATIVO",
    "TIPO OPERATIVO",
    "HORA INICIO",
    "HORA FIN",
    "DESPLIEGUE",
    "MOVILES",
    "SS.OO",
    "MOTOS",
    "HIPO",
    "PP.SS EN MOVIL",
    "PP.SS PIE TIERRA",
    "CHOQUE APOSTADO",
    "CHOQUE ALERTA",
    "GEO APOSTADO",
    "GEO ALERTA",
    "PP.SS TOTAL",
    "SECC.",
    "MATRICULA 1",
    "MATRICULA 2",
    "MATRICULA 3",
    "MATRICULA 4",
    "MATRICULA 5",
    "MATRICULA 6",
    "MATRICULA 7",
    "MATRICULA 8",
    "MATRICULA 9",
    "MATRICULA 10",
    "PORCENTAJE"
]

# Hojas esperadas en el archivo Excel
EXCEL_SHEETS = {
    "OPERATIVOS": "Hoja con información de despliegues operativos",
    "01": "Día 1 del mes",
    "02": "Día 2 del mes",
    "03": "Día 3 del mes",
    "04": "Día 4 del mes",
    "05": "Día 5 del mes",
    "06": "Día 6 del mes",
    "07": "Día 7 del mes",
    "08": "Día 8 del mes",
    "09": "Día 9 del mes",
    "10": "Día 10 del mes",
    "11": "Día 11 del mes",
    "12": "Día 12 del mes",
    "13": "Día 13 del mes",
    "14": "Día 14 del mes",
    "15": "Día 15 del mes",
    "16": "Día 16 del mes",
    "17": "Día 17 del mes",
    "18": "Día 18 del mes",
    "19": "Día 19 del mes",
    "20": "Día 20 del mes",
    "21": "Día 21 del mes",
    "22": "Día 22 del mes",
    "23": "Día 23 del mes",
    "24": "Día 24 del mes",
    "25": "Día 25 del mes",
    "26": "Día 26 del mes",
    "27": "Día 27 del mes",
    "28": "Día 28 del mes",
    "29": "Día 29 del mes",
    "30": "Día 30 del mes",
    "31": "Día 31 del mes"
}

# Información para la barra lateral
SIDEBAR_INFO = f"""
Esta aplicación permite convertir archivos Excel con información de despliegues operativos a formato PDF.

**Hojas esperadas en el Excel:**
{chr(10).join([f"- {hoja}: {desc}" for hoja, desc in EXCEL_SHEETS.items()])}

**Columnas esperadas en la hoja OPERATIVOS:**
{chr(10).join([f"- {col}" for col in EXPECTED_COLUMNS])}
"""

# Columnas numéricas para conversión automática
NUMERIC_COLUMNS = [
    "HORA INICIO",
    "HORA FIN",
    "DESPLIEGUE",
    "MOVILES",
    "SS.OO",
    "MOTOS",
    "HIPO",
    "PP.SS EN MOVIL",
    "PP.SS PIE TIERRA",
    "CHOQUE APOSTADO",
    "CHOQUE ALERTA",
    "GEO APOSTADO",
    "GEO ALERTA",
    "PP.SS TOTAL",
    "PORCENTAJE"
]

# Columnas que pueden contener múltiples valores separados por comas
MULTI_VALUE_COLUMNS = [
    "SECC."
]

# Copyright
COPYRIGHT = "© 2025 - Aplicación de Despliegues Operativos"
