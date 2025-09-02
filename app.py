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
        margin: 0;
        padding: 0;
    }

    .stApp {
        background-color: #f0f2f6;
    }

    .stApp > header {
        display: none; /* Oculta la cabecera por defecto de Streamlit */
    }

    .main-container {
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        height: 100vh;
        padding: 20px;
        box-sizing: border-box;
        text-align: center;
    }

    .title-container {
        display: flex;
        flex-direction: column;
        align-items: center;
        gap: 15px;
        margin-bottom: 20px;
    }

    .title {
        color: #004d99;
        font-weight: 700;
        font-size: 2.2em;
        margin: 0;
    }

    .stButton>button {
        background-color: #004d99;
        color: white;
        font-weight: 600;
        padding: 10px 24px;
        border: none;
        border-radius: 8px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        transition: background-color 0.3s ease;
    }

    .stButton>button:hover {
        background-color: #003366;
    }

    .stInfo {
        background-color: #e6f7ff;
        border-left: 5px solid #007bff;
        padding: 12px;
        border-radius: 8px;
        margin-top: 15px;
        text-align: left;
    }
"""

st.markdown(f"<style>{css_content}</style>", unsafe_allow_html=True)

# --- CONTENEDOR PRINCIPAL CON COLUMNAS PARA CENTRADO ---
col1, col2, col3 = st.columns([1, 4, 1])

with col2: # Centra el contenido en la columna del medio
    with st.container():
        st.markdown('<div class="main-container">', unsafe_allow_html=True)

        # --- CABECERA CON LOGO Y TÍTULO CENTRADOS ---
        st.markdown('<div class="title-container">', unsafe_allow_html=True)
        try:
            # Carga la imagen centrada
            st.image('imagen.png', width=150)
        except Exception as e:
            st.info("💡 Por favor, sube el archivo 'imagen.png' a tu repositorio de GitHub para que el logo aparezca.")

        st.markdown('<h1 class="title">AUTOMATIZACIÓN DE MEMORIAS TÉCNICAS</h1>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

        # --- DESCRIPCIÓN ---
        st.markdown("""
            <p style="text-align: center; color: #555; font-size: 1.1em; max-width: 600px;">
                Esta herramienta está diseñada para simplificar y acelerar la creación de tus memorias técnicas.<br>
                Haz clic en "Comenzar" para iniciar el proceso.
            </p>
        """, unsafe_allow_html=True)

        # --- BOTÓN DE COMENZAR CENTRADO ---
        st.button("Comenzar")

        st.markdown('</div>', unsafe_allow_html=True)
