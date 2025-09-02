import streamlit as st
import os

# --- CSS PERSONALIZADO ---
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Crea un archivo CSS en el mismo directorio.
# Este código se ejecuta cuando el usuario lo copia en el archivo style.css
# Esto es solo para que el código sea autónomo.
css_content = """
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;600;700&display=swap');

    body {
        font-family: 'Montserrat', sans-serif;
        background-color: #f0f2f6;
        color: #333;
    }

    .stApp {
        background-color: #f0f2f6;
    }

    .stApp > header {
        background-color: #ffffff;
        padding: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        border-radius: 10px;
        margin-bottom: 20px;
    }

    .title-container {
        display: flex;
        align-items: center;
        gap: 20px;
        padding: 20px;
    }

    .logo-img {
        border-radius: 8px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }

    .st-emotion-cache-1jmveo6 {
        display: flex;
        align-items: center;
        justify-content: center;
    }
"""

st.markdown(f"<style>{css_content}</style>", unsafe_allow_html=True)

# --- CABECERA CON LOGO Y TÍTULO ---
col1, col2 = st.columns([3, 1])

with col1:
    st.markdown("""
        <h1 style="color: #004d99; font-weight: 700; font-size: 2.5em;">AUTOMATIZACIÓN DE MEMORIAS TÉCNICAS</h1>
    """, unsafe_allow_html=True)
with col2:
    try:
        # La forma correcta de cargar una imagen localmente en Streamlit
        st.image('imagen.png', width=150)
    except Exception as e:
        st.error(f"Error al cargar la imagen: {e}")
        st.info("Por favor, asegúrate de que el archivo 'imagen.png' esté en el repositorio de GitHub, en la misma carpeta que 'app.py'.")

st.markdown("""<hr style="border: 2px solid #004d99; margin: 20px 0;">""", unsafe_allow_html=True)


# --- CONTENIDO DE LA PÁGINA ---
st.subheader("¡Bienvenido al asistente de memorias técnicas!")
st.write("Esta herramienta está diseñada para simplificar y acelerar la creación de tus memorias técnicas. Usa el menú lateral para navegar por las diferentes funcionalidades.")

st.markdown("---")

st.markdown("""
### ¿Qué puedes esperar?
- **Agilidad**: Reduce el tiempo de redacción de documentos complejos.
- **Precisión**: Genera contenido basado en datos y directrices predefinidas.
- **Colaboración**: Permite un flujo de trabajo más eficiente con tu equipo.
""")
