# Conversor de Despliegues Operativos Excel a PDF

Esta aplicación permite cargar archivos Excel con información de despliegues operativos y convertirlos a formato PDF para su fácil distribución y visualización. Diseñada específicamente para la Guardia Republicana, facilita la generación de informes profesionales con un diseño adaptado a los estándares institucionales.

## Características

- Interfaz sencilla y amigable desarrollada con Streamlit
- Carga de archivos Excel con datos de despliegues operativos
- Selección de hojas en archivos Excel con múltiples hojas
- Vista previa de los datos cargados
- Generación de PDF con formato profesional y encabezado institucional
- Organización de datos por unidad para mejor visualización
- Combinación de columnas "NOMBRE ORDEN" y "NOMBRE OPERATIVO" para mayor claridad
- Iconos visuales para las columnas de recursos (móviles, motos, personal, etc.)
- Descarga inmediata del PDF generado

## Requisitos

- Python 3.7 o superior
- Anaconda o Miniconda (recomendado para optimizaciones de rendimiento)
- Dependencias listadas en `requirements.txt`:
  - streamlit
  - pandas
  - reportlab
  - svglib
  - fpdf2
  - pillow
  - openpyxl

## Instalación

### Opción 1: Instalación con Anaconda (Recomendado)

1. Clone o descargue este repositorio
2. Cree un entorno Anaconda e instale las dependencias:

```bash
# Crear un nuevo entorno
conda create -n despliegues_pdf python=3.8
conda activate despliegues_pdf

# Instalar dependencias
conda install -c conda-forge streamlit pandas reportlab pillow
conda install -c conda-forge svglib fpdf2 openpyxl
```

### Opción 2: Instalación con pip

1. Clone o descargue este repositorio
2. Instale las dependencias:

```bash
pip install -r requirements.txt
```

## Estructura del Proyecto

El proyecto está organizado de manera modular para facilitar su mantenimiento y extensión:

- **app.py**: Aplicación principal con la interfaz de Streamlit
- **app_simple.py**: Versión simplificada de la aplicación
- **config.py**: Configuraciones generales de la aplicación
- **pdf_config.py**: Configuraciones específicas para la generación de PDFs
- **pdf_generator.py**: Lógica principal para la generación de PDFs
- **pdf_header_footer.py**: Funciones para crear encabezados y pies de página
- **pdf_styles.py**: Estilos para las tablas y elementos del PDF
- **pdf_table_utils.py**: Utilidades para la creación de tablas
- **unidades_config.py**: Configuración de unidades para la organización de datos
- **utils.py**: Funciones auxiliares para procesamiento de datos
- **images/**: Directorio con imágenes e iconos utilizados en el PDF

## Uso

1. Ejecute la aplicación:

```bash
# Si usa Anaconda
conda activate despliegues_pdf
streamlit run app.py

# Si usa Python estándar
streamlit run app.py
```

2. Abra su navegador web en la dirección indicada (generalmente http://localhost:8501)
3. Cargue su archivo Excel utilizando el botón de carga
4. Si el archivo tiene múltiples hojas, seleccione la hoja "OPERATIVOS"
5. Verifique la vista previa de los datos
6. Seleccione si desea organizar por unidad (recomendado)
7. Haga clic en "Generar PDF"
8. Descargue el PDF generado

## Formato del Excel

El archivo Excel debe contener una hoja llamada "OPERATIVOS" con las siguientes columnas:

- **UNIDAD**: Identificador de la unidad (ej: "GR1", "GR2", etc.)
- **TIPO ORDEN**: Tipo de orden operativa
- **NUMERO ORDEN**: Número de la orden
- **NOMBRE ORDEN**: Nombre de la orden operativa
- **NOMBRE OPERATIVO**: Nombre del operativo
- **TIPO OPERATIVO**: Tipo de operativo (nueva columna)
- **HORA INICIO**: Hora de inicio del despliegue
- **HORA FIN**: Hora de finalización del despliegue
- **MOVILES**: Cantidad de vehículos
- **SS.OO**: Cantidad de suboficiales
- **MOTOS**: Cantidad de motocicletas
- **HIPO**: Cantidad de caballos
- **PP.SS EN MOVIL**: Personal en vehículos
- **PP.SS PIE TIERRA**: Personal a pie
- **CHOQUE APOSTADO**: Personal de choque apostado
- **CHOQUE ALERTA**: Personal de choque en alerta
- **GEO APOSTADO**: Personal GEO apostado
- **GEO ALERTA**: Personal GEO en alerta
- **PP.SS TOTAL**: Total de personal
- **SECC.**: Sección

## Personalización

El sistema permite personalizar varios aspectos:

### Unidades

Para modificar las unidades y su orden de aparición, edite el archivo `unidades_config.py`:

```python
# Mapeo de códigos de unidad a nombres completos
UNIDADES_NOMBRES = {
    "GR1": "Guardia Republicana 1",
    "GR2": "Guardia Republicana 2",
    # Añada más unidades según sea necesario
}

# Orden de las unidades en el PDF
ORDEN_UNIDADES = ["GR1", "GR2", ...]
```

### Columnas e Iconos

Para modificar las columnas que aparecen en el PDF y sus iconos asociados, edite `pdf_config.py`:

```python
# Columnas a incluir en el PDF
COLUMNAS_PDF = ["UNIDAD", "NOMBRE ORDEN", ...]

# Iconos para columnas específicas
ICONOS_COLUMNAS = {
    "MOVILES": "images/icono_movil.png",
    "MOTOS": "images/icono_moto.png",
    # Añada más iconos según sea necesario
}
```

## Mantenimiento y Desarrollo

El código está diseñado de manera modular para facilitar su mantenimiento y extensión. Las principales funciones están documentadas con docstrings detallados que explican su propósito, parámetros y valores de retorno.

## Notas

### Encabezado Personalizado

El PDF generado incluye un encabezado institucional con los siguientes elementos:

- Logo de la Guardia Republicana (logo-gr-dorado.svg) en la esquina derecha
- Fecha en formato largo en español (ej: "17 de marzo de 2025") en la esquina izquierda
- Hora en formato 24h (ej: "19:30") debajo de la fecha
- Título "DIRECCIÓN NACIONAL GUARDIA REPUBLICANA" centrado en color dorado
- Subtítulo "Estado Mayor Policial" centrado debajo del título
- Línea horizontal dorada debajo del encabezado

Para modificar este encabezado, edite el archivo `pdf_header_footer.py`.

### Rendimiento

La aplicación está optimizada para manejar grandes cantidades de datos. La función `generar_pdf_optimizado` ha sido refactorizada en subfunciones más pequeñas para mejorar la legibilidad y el mantenimiento del código.

### Contribuciones

Si desea contribuir a este proyecto, por favor asegúrese de seguir las convenciones de código existentes y documentar adecuadamente cualquier nueva funcionalidad.

- Los archivos generados se guardan con el nombre "despliegues_operativos.pdf"

## Despliegue en Producción

Para desplegar esta aplicación en un entorno de producción, se recomienda utilizar Anaconda/Miniconda para aprovechar las optimizaciones de rendimiento en las bibliotecas científicas como pandas.

### Pasos para Despliegue con Anaconda

1. Instalar Miniconda en el servidor de producción:
   ```bash
   # En Linux
   wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
   bash Miniconda3-latest-Linux-x86_64.sh
   
   # En Windows
   # Descargar e instalar desde https://docs.conda.io/en/latest/miniconda.html
   ```

2. Crear el entorno y instalar dependencias:
   ```bash
   conda create -n despliegues_pdf python=3.8
   conda activate despliegues_pdf
   conda install -c conda-forge streamlit pandas reportlab pillow svglib fpdf2 openpyxl
   ```

3. Ejecutar la aplicación:
   ```bash
   streamlit run app.py
   ```

4. Para servir la aplicación en producción, considere usar herramientas como nginx como proxy inverso y systemd para gestionar el proceso.
