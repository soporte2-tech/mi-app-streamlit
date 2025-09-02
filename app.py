import streamlit as st

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(layout="wide")

# --- CSS FINAL Y DEFINITIVO ---
css_final = """
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;600;700&display=swap');

    /* Ocultar elementos de Streamlit que no queremos */
    .stApp > header, #MainMenu, footer {
        visibility: hidden;
    }

    /* Fondo general de la aplicación */
    .stApp {
        background-color: #f0f2f6;
        font-family: 'Montserrat', sans-serif;
    }

    /* La "Tarjeta" que contendrá todo nuestro contenido */
    /* Este div será creado con st.markdown para envolver todo */
    .card-container {
        background-color: white;
        padding: 40px;
        border-radius: 15px;
        box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1);
        text-align: center;
        margin-top: 5rem;
    }
    
    /* Estilo del título principal */
    .title {
        color: #1E3A5F;
        font-weight: 700;
        font-size: clamp(1.8rem, 4vw, 2.5rem); /* Título responsive */
        letter-spacing: -1px;
        margin-top: 20px;
        margin-bottom: 20px;
        line-height: 1.2;
    }
    
    /* Estilo de la descripción */
    .description {
        color: #555;
        font-size: clamp(1rem, 2.5vw, 1.1rem); /* Texto responsive */
        line-height: 1.6;
        margin-bottom: 30px;
    }

    /* Estilo del botón */
    .stButton>button {
        background-color: #0056b3;
        color: white;
        font-weight: 600;
        font-size: 1em;
        padding: 12px 30px;
        border: none;
        border-radius: 8px;
        box-shadow: 0 4px 10px rgba(0, 86, 179, 0.2);
        transition: all 0.3s ease;
        width: 100%; /* El botón ocupará todo el ancho de su columna */
    }

    .stButton>button:hover {
        background-color: #004494;
        transform: scale(1.05);
        box-shadow: 0 6px 15px rgba(0, 86, 179, 0.3);
    }
"""
st.markdown(f"<style>{css_final}</style>", unsafe_allow_html=True)

# --- LAYOUT CON COLUMNAS PARA CENTRADO ---
# Usamos columnas para centrar horizontalmente todo el bloque de la tarjeta
col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    # Usamos un markdown para abrir un div que actuará como nuestro contenedor de tarjeta
    st.markdown('<div class="card-container">', unsafe_allow_html=True)

    # LOGO (usando st.image para que se cargue correctamente)
    try:
        st.image('imagen.png', width=150)
    except Exception as e:
        st.warning("⚠️ No se encontró la imagen 'imagen.png'.")

    # TÍTULO (usando st.markdown)
    st.markdown('<h1 class="title">AUTOMATIZACIÓN DE MEMORIAS TÉCNICAS</h1>', unsafe_allow_html=True)

    # DESCRIPCIÓN (usando st.markdown)
    st.markdown("""
        <p class="description">
            Esta herramienta está diseñada para simplificar y acelerar la creación de tus memorias técnicas.
            <br>
            Haz clic en <b>Comenzar</b> para iniciar el proceso.
        </p>
    """, unsafe_allow_html=True)

    # --- CENTRADO DEL BOTÓN DENTRO DE LA TARJETA ---
    # Creamos un sub-layout de columnas solo para el botón
    b_col1, b_col2, b_col3 = st.columns([1, 1.5, 1])
    with b_col2:
        if st.button("Comenzar"):
            st.success("¡Proceso iniciado!")

    # Cerramos el div de nuestro contenedor de tarjeta
    st.markdown('</div>', unsafe_allow_html=True)
