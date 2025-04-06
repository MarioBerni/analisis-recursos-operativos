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
    "SECC."
]

# Hojas esperadas en el archivo Excel
EXCEL_SHEETS = {
    "OPERATIVOS": "Hoja con información de despliegues operativos"
    # Aquí se pueden agregar más hojas según sea necesario
}

# Información para la barra lateral
SIDEBAR_INFO = f"""
Esta aplicación permite convertir archivos Excel con información de despliegues operativos a formato PDF.

**Hojas esperadas en el Excel:**
{chr(10).join([f"- {hoja}: {desc}" for hoja, desc in EXCEL_SHEETS.items()])}

**Columnas esperadas en la hoja OPERATIVOS:**
{chr(10).join([f"- {col}" for col in EXPECTED_COLUMNS])}
"""

# Copyright
COPYRIGHT = "© 2025 - Aplicación de Despliegues Operativos"
