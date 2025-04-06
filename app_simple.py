import streamlit as st
import pandas as pd
import io
import os
from fpdf import FPDF
from unidades_config import UNIDADES_ORDEN, UNIDADES_NOMBRES

# Configuración de la página de Streamlit
st.set_page_config(
    page_title="Conversor CSV a PDF - Despliegues Operativos",
    page_icon="📊",
    layout="wide"
)

# Título y descripción
st.title("Conversor de Despliegues Operativos CSV a PDF")
st.markdown("Esta aplicación permite cargar un archivo CSV con información de despliegues operativos y convertirlo a PDF.")

# Sección para cargar el archivo CSV
st.header("1. Cargar archivo CSV")
uploaded_file = st.file_uploader("Seleccione el archivo CSV con los datos de despliegues operativos", type=['csv'])

# Sección de opciones de organización
st.header("2. Opciones de organización")
st.subheader("Organizar por:")
organizar_por_unidad = st.checkbox("Unidad", value=True, help="Organiza las tablas por unidad")

# Función para procesar el CSV y generar el PDF
def generar_pdf_optimizado(csv_data, organizar_por_unidad):
    # Crear un buffer para el PDF
    buffer = io.BytesIO()
    
    # Leer el CSV
    df = pd.read_csv(io.StringIO(csv_data.decode('utf-8')), delimiter='\t')
    
    # Configurar el PDF
    pdf = FPDF(orientation='L', unit='mm', format='A4')
    pdf.add_page()
    
    # Añadir título
    pdf.set_font('Arial', 'B', 16)
    pdf.cell(0, 10, 'Informe de Despliegues Operativos', 0, 1, 'C')
    pdf.ln(5)
    
    # Configurar la tabla
    pdf.set_font('Arial', 'B', 8)
    
    # Calcular ancho de columnas (ajustar según necesidad)
    col_width = 260 / len(df.columns)
    
    # Encabezados
    for header in df.columns:
        pdf.cell(col_width, 10, header, 1, 0, 'C')
    pdf.ln()
    
    # Datos
    pdf.set_font('Arial', '', 7)
    if organizar_por_unidad:
        for unidad in UNIDADES_ORDEN:
            df_unidad = df[df['UNIDAD'] == unidad]
            if not df_unidad.empty:
                pdf.set_font('Arial', 'B', 10)
                pdf.cell(0, 10, f"Unidad: {UNIDADES_NOMBRES[unidad]}", 0, 1, 'L')
                pdf.ln()
                for index, row in df_unidad.iterrows():
                    for item in row:
                        pdf.cell(col_width, 7, str(item), 1, 0, 'C')
                    pdf.ln()
                pdf.ln()
    else:
        for index, row in df.iterrows():
            for item in row:
                pdf.cell(col_width, 7, str(item), 1, 0, 'C')
            pdf.ln()
    
    # Guardar PDF en el buffer
    pdf.output(buffer)
    buffer.seek(0)
    return buffer

if uploaded_file is not None:
    try:
        # Leer el contenido del archivo
        csv_data = uploaded_file.getvalue()
        
        # Mostrar los datos cargados
        st.header("3. Vista previa de los datos")
        df = pd.read_csv(io.StringIO(csv_data.decode('utf-8')), delimiter='\t')
        st.dataframe(df.head(10))  # Mostrar solo las primeras 10 filas
        
        # Botón para generar y descargar el PDF
        st.header("4. Generar y descargar PDF")
        if st.button("Generar PDF"):
            with st.spinner("Generando PDF..."):
                # Generar PDF según las opciones seleccionadas
                pdf_bytes = generar_pdf_optimizado(csv_data, organizar_por_unidad=organizar_por_unidad)
                
                # Proporcionar el PDF para descarga
                st.download_button(
                    label="📥 Descargar PDF",
                    data=pdf_bytes,
                    file_name="despliegues_operativos.pdf",
                    mime="application/pdf"
                )
                
                st.success("¡PDF generado con éxito! Haga clic en el botón de descarga para obtener el archivo.")
    
    except Exception as e:
        st.error(f"Error al procesar el archivo: {e}")
        st.info("Asegúrese de que el archivo CSV tenga el formato correcto con las columnas especificadas.")

# Información adicional
st.sidebar.header("Información")
st.sidebar.info("""
Esta aplicación permite convertir archivos CSV con información de despliegues operativos a formato PDF.

**Formato esperado del CSV:**
- UNIDAD
- TIPO ORDEN
- NUMERO ORDEN
- NOMBRE ORDEN
- NOMBRE OPERATIVO
- HORA INICIO
- HORA FIN
- MÓVILES
- SS.OO
- MOTOS
- HIPO
- PP.SS EN MÓVIL
- PP.SS PIE TIERRA
- CHOQUE APOSTADO
- CHOQUE ALERTA
- GEO APOSTADO
- GEO ALERTA
- PP.SS TOTAL
- SECC.
""")

# Información sobre las unidades
st.sidebar.header("Unidades")
st.sidebar.info("""
**Organización por unidades:**
""" + "\n".join([f"- {unidad}: {UNIDADES_NOMBRES[unidad]}" for unidad in UNIDADES_ORDEN]))

st.sidebar.markdown("---")
st.sidebar.markdown("© 2025 - Aplicación de Despliegues Operativos")
