import streamlit as st

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(layout="wide")

# --- CSS FINAL Y DEFINITIVO ---
# Este CSS es más específico para asegurar que se aplique correctamente.
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
    
    /* LA CLAVE: Aplicamos el estilo de la tarjeta al contenedor de Streamlit */
    /* Este selector es robusto y apunta al contenedor que creamos con st.container */
    [data-testid="stVerticalBlock"] .st-emotion-cache-1jicfl2 {
        background-color: white; /* 1. Fondo blanco */
        padding: 40px;
        border-radius: 15px;
        box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1);
        margin-top: 4rem;
        border: none; /* Quitamos el borde gris por defecto del contenedor */
        
        /* 2. Centramos todo el contenido verticalmente */
        display: flex;
        flex-direction: column;
        align-items: center; /* ESTO CENTRA TODO HORIZONTALMENTE */
        gap: 20px; /* Espacio uniforme entre elementos */
    }
    
    /* Estilos para el texto y el botón (sin cambios) */
    .title {
        color: #1E3A5F;
        font-weight: 700;
        font-size: clamp(1.8rem, 4vw, 2.5rem);
        letter-spacing: -1px;
        line-height: 1.2;
        margin: 0;
        text-align: center;
    }
    
    .description {
        color: #555;
        font-size: clamp(1rem, 2.5vw, 1.1rem);
        line-height: 1.6;
        margin: 0;
        text-align: center;
    }

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
    }

    .stButton>button:hover {
        background-color: #004494;
        transform: scale(1.05);
        box-shadow: 0 6px 15px rgba(0, 86, 179, 0.3);
    }
"""
st.markdown(f"<style>{css_final}</style>", unsafe_allow_html=True)

# --- LAYOUT CON COLUMNAS PARA CENTRADO HORIZONTAL DE LA TARJETA ---
col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    # Creamos un contenedor nativo de Streamlit. El CSS de arriba lo convertirá
    # en nuestra tarjeta blanca y centrará todo su contenido.
    with st.container(border=True):

        # LOGO
        st.image('imagen.png', width=150)

        # TÍTULO
        st.markdown('<h1 class="title">AUTOMATIZACIÓN DE MEMORIAS TÉCNICAS</h1>', unsafe_allow_html=True)

        # DESCRIPCIÓN
        st.markdown("""
            <p class="description">
                Esta herramienta está diseñada para simplificar y acelerar la creación de tus memorias técnicas.
                <br>
                Haz clic en <b>Comenzar</b> para iniciar el proceso.
            </p>
        """, unsafe_allow_html=True)

        # BOTÓN
        if st.button("Comenzar"):
            st.success("¡Proceso iniciado!")
