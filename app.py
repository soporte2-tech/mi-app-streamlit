import streamlit as st
import base64

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(layout="wide")

# --- FUNCIÓN PARA CARGAR IMAGEN COMO BASE64 ---
# Esto hace que la imagen se cargue siempre, sin problemas de ruta.
def get_image_as_base64(path):
    try:
        with open(path, "rb") as f:
            data = f.read()
        return base64.b64encode(data).decode()
    except IOError:
        return None

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
    .card {
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
        font-size: clamp(1.8rem, 4vw, 2.5rem);
        letter-spacing: -1px;
        margin-top: 20px;
        margin-bottom: 20px;
        line-height: 1.2;
    }
    
    /* Estilo de la descripción */
    .description {
        color: #555;
        font-size: clamp(1rem, 2.5vw, 1.1rem);
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
    }

    .stButton>button:hover {
        background-color: #004494;
        transform: scale(1.05);
        box-shadow: 0 6px 15px rgba(0, 86, 179, 0.3);
    }
"""
st.markdown(f"<style>{css_final}</style>", unsafe_allow_html=True)

# --- LAYOUT CON COLUMNAS PARA CENTRADO ---
col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    # Usamos un único st.markdown para crear toda la tarjeta y su contenido.
    # Esto nos da control total sobre el HTML y evita los errores de Streamlit.
    
    img_base64 = get_image_as_base64("imagen.png")
    
    if img_base64:
        # Si la imagen se carga, la mostramos
        image_html = f'<img src="data:image/png;base64,{img_base64}" width="150">'
    else:
        # Si no, mostramos un aviso
        image_html = '<div style="background-color:#ffcccc;color:#a00;padding:10px;border-radius:5px;">⚠️ No se encontró la imagen \'imagen.png\'. Súbela a GitHub.</div>'

    card_html = f"""
    <div class="card">
        {image_html}
        <h1 class="title">AUTOMATIZACIÓN DE MEMORIAS TÉCNICAS</h1>
        <p class="description">
            Esta herramienta está diseñada para simplificar y acelerar la creación de tus memorias técnicas.
            <br>
            Haz clic en <b>Comenzar</b> para iniciar el proceso.
        </p>
    </div>
    """
    st.markdown(card_html, unsafe_allow_html=True)

    # El botón se coloca fuera del markdown, pero visualmente se alineará correctamente.
    if st.button("Comenzar"):
        st.success("¡Proceso iniciado!")
