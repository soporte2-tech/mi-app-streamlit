import streamlit as st
import os

# --- 1. CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(layout="wide")

# --- 2. CSS MÍNIMO Y EFECTIVO ---
css_simple = """
    /* Fondo blanco para toda la app */
    .stApp {
        background-color: white;
    }

    /* Ocultar la cabecera y el pie de página de Streamlit */
    .stApp > header, #MainMenu, footer {
        visibility: hidden;
    }

    /* Estilo profesional para el botón */
    .stButton > button {
        background-color: #0056b3;
        color: white;
        font-weight: 600;
        font-size: 1.1em;
        padding: 12px 35px;
        border: none;
        border-radius: 8px;
        box-shadow: 0 4px 10px rgba(0, 86, 179, 0.2);
        transition: all 0.3s ease;
    }

    .stButton > button:hover {
        background-color: #004494;
        transform: scale(1.05);
    }
    
    /* Centrado del contenido principal */
    .content-container {
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        height: 100vh;
        width: 100%;
        text-align: center;
    }

    /* Estilo para el título */
    .title-h1 {
        font-family: 'Montserrat', sans-serif;
        color: #1E3A5F;
        font-size: 2.5em;
        font-weight: bold;
        margin-top: 0;
        margin-bottom: 0.5em;
    }
"""
st.markdown(f"<style>{css_simple}</style>", unsafe_allow_html=True)

# --- LAYOUT CENTRADO CON CONTENEDOR ---
_, col2, _ = st.columns([1, 2, 1])

with col2:
    with st.container():
        # Contenedor que centra el contenido en la columna
        st.markdown('<div class="content-container">', unsafe_allow_html=True)
        
        # LOGO CENTRADO
        _, logo_col, _ = st.columns([1, 1, 1])
        with logo_col:
            try:
                st.image('imagen.png', width=150)
            except Exception:
                st.warning("⚠️ No se encontró la imagen 'imagen.png'.")

        # TÍTULO GRANDE Y CENTRADO
        st.markdown("<h1 class='title-h1'>AUTOMATIZACIÓN DE MEMORIAS TÉCNICAS</h1>", unsafe_allow_html=True)
        st.write("")  # Espacio

        # DESCRIPCIÓN CENTRADA
        st.markdown("""
        <p style='text-align: center; font-size: 1.1em; color: #555;'>
            Esta herramienta está diseñada para simplificar y acelerar la creación de tus memorias técnicas.
            <br>
            Haz clic en <b>Comenzar</b> para iniciar el proceso.
        </p>
        """, unsafe_allow_html=True)
        st.write("") # Espacio
        
        # BOTÓN CENTRADO
        _, btn_col, _ = st.columns([1, 1, 1])
        with btn_col:
            if st.button("Comenzar"):
                st.success("¡Proceso iniciado!")

        st.markdown("</div>", unsafe_allow_html=True)
