import streamlit as st

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
    .stButton>button {
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

    .stButton>button:hover {
        background-color: #004494;
        transform: scale(1.05);
    }
"""
st.markdown(f"<style>{css_simple}</style>", unsafe_allow_html=True)

# --- 3. LAYOUT CENTRADO ---
# Usamos columnas para crear un espacio central donde vivirá todo nuestro contenido.
_ , col2, _ = st.columns([1, 2, 1])

with col2:
    # --- 4. CONTENIDO DE LA PÁGINA ---
    
    # === LA CORRECCIÓN ESTÁ AQUÍ ===
    # LOGO CENTRADO USANDO COLUMNAS
    _ , logo_col, _ = st.columns([1, 1, 1])
    with logo_col:
        try:
            st.image('imagen.png', width=150)
        except Exception:
            st.warning("⚠️ No se encontró la imagen 'imagen.png'.")

    # TÍTULO GRANDE Y CENTRADO
    st.markdown("<h1 style='text-align: center; color: #1E3A5F;'>AUTOMATIZACIÓN DE MEMORIAS TÉCNICAS</h1>", unsafe_allow_html=True)
    
    # Párrafo de espacio
    st.write("") 

    # DESCRIPCIÓN CENTRADA
    st.markdown("""
    <p style='text-align: center; font-size: 1.1em; color: #555;'>
        Esta herramienta está diseñada para simplificar y acelerar la creación de tus memorias técnicas.
        <br>
        Haz clic en <b>Comenzar</b> para iniciar el proceso.
    </p>
    """, unsafe_allow_html=True)
    
    # Párrafo de espacio
    st.write("")
    st.write("")

    # BOTÓN CENTRADO
    _ , btn_col, _ = st.columns([1, 1, 1])
    with btn_col:
        if st.button("Comenzar"):
            st.success("¡Proceso iniciado!")
