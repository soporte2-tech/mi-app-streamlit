import streamlit as st
import os

# --- CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(layout="wide") # Aprovechamos el ancho completo

# --- CSS MEJORADO ---
# Este CSS introduce un diseño de tarjeta, mejora la tipografía y añade micro-interacciones.
css_mejorado = """
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;600;700&display=swap');

    /* Oculta elementos por defecto de Streamlit que no necesitamos */
    .stApp > header {
        display: none;
    }
    #MainMenu {
        display: none;
    }
    footer {
        display: none;
    }

    /* Contenedor principal para centrar la tarjeta vertical y horizontalmente */
    .stApp {
        display: flex;
        justify-content: center;
        align-items: center;
        background-color: #f0f2f6; /* Un gris claro para el fondo */
        font-family: 'Montserrat', sans-serif;
        height: 100vh; /* Ocupa toda la altura de la ventana */
    }

    /* La "Tarjeta" que contendrá todo */
    .card {
        background-color: white;
        padding: 40px;
        border-radius: 15px;
        box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1);
        text-align: center;
        max-width: 650px; /* Ancho máximo de la tarjeta */
        width: 90%;
        display: flex;
        flex-direction: column;
        align-items: center;
        gap: 20px; /* Espacio entre los elementos dentro de la tarjeta */
    }

    /* Estilo del logo */
    .logo-img {
        width: 150px;
        margin-bottom: 10px;
    }

    /* Estilo del título principal */
    .title {
        color: #1E3A5F; /* Un azul oscuro más sobrio */
        font-weight: 700;
        font-size: 2.5em;
        letter-spacing: -1px; /* Un poco más juntas las letras, más moderno */
        margin: 0;
    }
    
    /* Estilo de la descripción */
    .description {
        color: #555;
        font-size: 1.1em;
        line-height: 1.6; /* Mayor interlineado para fácil lectura */
        margin: 0;
    }

    /* Estilo del botón */
    .stButton>button {
        background-color: #0056b3; /* Un azul más vibrante */
        color: white;
        font-weight: 600;
        font-size: 1em;
        padding: 12px 30px;
        border: none;
        border-radius: 8px;
        box-shadow: 0 4px 10px rgba(0, 86, 179, 0.2);
        transition: all 0.3s ease; /* Transición suave para todos los efectos */
        margin-top: 15px; /* Espacio extra arriba del botón */
    }

    .stButton>button:hover {
        background-color: #004494; /* Azul más oscuro al pasar el ratón */
        transform: scale(1.05); /* Efecto de crecimiento sutil */
        box-shadow: 0 6px 15px rgba(0, 86, 179, 0.3);
    }
"""

st.markdown(f"<style>{css_mejorado}</style>", unsafe_allow_html=True)

# --- CONTENIDO DE LA APP DENTRO DE UNA "TARJETA" ---

# Usamos st.markdown para crear el contenedor principal (la tarjeta)
st.markdown('<div class="card">', unsafe_allow_html=True)

# --- LOGO ---
try:
    # Usamos una clase para poder estilizar la imagen si es necesario
    st.image('imagen.png', width=150)
except Exception as e:
    st.warning("⚠️ No se encontró 'imagen.png'. Sube el logo a tu repositorio de GitHub.")

# --- TÍTULO ---
st.markdown('<h1 class="title">AUTOMATIZACIÓN DE MEMORIAS TÉCNICAS</h1>', unsafe_allow_html=True)

# --- DESCRIPCIÓN ---
st.markdown("""
    <p class="description">
        Esta herramienta está diseñada para simplificar y acelerar la creación de tus memorias técnicas.
        <br>
        Haz clic en <b>Comenzar</b> para iniciar el proceso.
    </p>
""", unsafe_allow_html=True)

# --- BOTÓN DE ACCIÓN ---
if st.button("Comenzar"):
    # Aquí puedes añadir la lógica que se ejecutará al hacer clic
    st.success("¡Proceso iniciado!") 
    # (En una app real, aquí navegarías a otra página o mostrarías nuevos elementos)

# Cerramos el div de la tarjeta
st.markdown('</div>', unsafe_allow_html=True)
