import streamlit as st

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(layout="wide")

# --- CSS DEFINITIVO ---
css_final = """
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;600;700&display=swap');

    /* Ocultar elementos de Streamlit */
    .stApp > header, #MainMenu, footer {
        visibility: hidden;
    }

    /* Fondo general */
    .stApp {
        background-color: #f0f2f6;
        font-family: 'Montserrat', sans-serif;
    }

    /* CONTENEDOR TARJETA */
    .card {
        background-color: white;
        border-radius: 15px;
        padding: 40px;
        margin-top: 4rem;
        text-align: center;
        box-shadow: 0 10px 25px rgba(0,0,0,0.1);
    }

    /* Logo centrado */
    .card img {
        display: block;
        margin-left: auto;
        margin-right: auto;
    }

    /* Título */
    .title {
        color: #1E3A5F;
        font-weight: 700;
        font-size: clamp(1.8rem, 4vw, 2.5rem);
        margin: 20px 0;
    }

    /* Descripción */
    .description {
        color: #555;
        font-size: clamp(1rem, 2.5vw, 1.1rem);
        margin-bottom: 30px;
    }

    /* Botón */
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
        margin: auto; /* centra horizontalmente */
        display: block; /* hace que respete el centrado */
    }
    .stButton>button:hover {
        background-color: #004494;
        transform: scale(1.05);
        box-shadow: 0 6px 15px rgba(0, 86, 179, 0.3);
    }
"""
st.markdown(f"<style>{css_final}</style>", unsafe_allow_html=True)

# --- LAYOUT ---
col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    st.markdown('<div class="card">', unsafe_allow_html=True)

    # LOGO
    st.image("imagen.png", width=150)


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

    st.markdown('</div>', unsafe_allow_html=True)
