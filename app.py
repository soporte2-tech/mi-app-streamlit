import streamlit as st
from PIL import Image

# Configuración de la página
st.set_page_config(
    page_title="Automatización de Memorias Técnicas",
    page_icon="🔧",
    layout="wide"
)

# Título de la aplicación
st.title("AUTOMATIZACIÓN DE MEMORIAS TÉCNICAS")

# Logo de la empresa
try:
    # Carga la imagen desde la misma carpeta que el script
    logo = Image.open('imagen.png')
    st.image(logo, width=200)
except FileNotFoundError:
    st.error("Error: El archivo 'imagen.png' no se encontró.")
    st.info("Por favor, asegúrate de que el archivo 'imagen.png' esté en la misma carpeta que este script.")
except Exception as e:
    st.error(f"Error al cargar la imagen: {e}")
    st.info("Asegúrate de que la imagen sea un formato válido (como PNG, JPG, etc.).")

# Espacio en blanco para la siguiente sección
st.subheader("¡Bienvenido!")
st.write("Esta es la página de inicio de la aplicación.")
st.markdown("---")
