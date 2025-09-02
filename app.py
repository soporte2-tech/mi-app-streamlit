import streamlit as st

# --- CONFIGURACIÓN DE PÁGINA ---
# Usar layout "wide" para tener más control
st.set_page_config(layout="wide")

# --- CSS CORREGIDO Y MÁS ROBUSTO ---
css_robusto = """
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;600;700&display=swap');

    /* Ocultar elementos de Streamlit que no queremos */
    .stApp > header, #MainMenu, footer {
        display: none;
    }

    /* Fondo general de la aplicación */
    .stApp {
        background-color: #f0f2f6;
        font-family: 'Montserrat', sans-serif;
    }

    /* La "Tarjeta" que contendrá todo nuestro contenido */
    .card {
        background-color: white;
        padding: 40px;
        border-radius: 15px;
        box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1);
        text-align: center;
        display: flex;
        flex-direction: column;
        align-items: center;
        gap: 20px; /* Espacio uniforme entre elementos */
        margin-top: 5rem; /* Margen superior para centrar verticalmente */
    }

    /* Estilo del título principal */
    .title {
        color: #1E3A5F;
        font-weight: 700;
        font-size: clamp(1.8rem, 4vw, 2.5rem); /* Título responsive */
        letter-spacing: -1px;
        margin: 0;
        line-height: 1.2;
    }
    
    /* Estilo de la descripción */
    .description {
        color: #555;
        font-size: clamp(1rem, 2.5vw, 1.1rem); /* Texto responsive */
        line-height: 1.6;
        margin: 0;
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
        margin-top: 15px;
    }

    .stButton>button:hover {
        background-color: #004494;
        transform: scale(1.05);
        box-shadow: 0 6px 15px rgba(0, 86, 179, 0.3);
    }
"""

st.markdown(f"<style>{css_robusto}</style>", unsafe_allow_html=True)

# --- LAYOUT CON COLUMNAS PARA CENTRADO PERFECTO ---
# Creamos tres columnas: [espacio_izq, contenido_central, espacio_der]
# El número '3' en el medio hace que la columna central sea 3 veces más ancha que los lados.
col1, col2, col3 = st.columns([1, 3, 1])

# Todo nuestro contenido va DENTRO de la columna 2 (col2)
with col2:
    # Envolvemos todo en un contenedor para aplicar la clase "card"
    with st.container():
        st.markdown('<div class="card">', unsafe_allow_html=True)

        # LOGO
        try:
            st.image('imagen.png', width=150)
        except Exception as e:
            st.warning("⚠️ No se encontró 'imagen.png'. Sube el logo a tu repositorio de GitHub.")

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

        # BOTÓN DE ACCIÓN
        if st.button("Comenzar"):
            st.success("¡Proceso iniciado!")

        # Cierre del div de la tarjeta
        st.markdown('</div>', unsafe_allow_html=True)
