import streamlit as st
import time

# --- 1. CONFIGURACIÓN DE LA PÁGINA Y ESTILOS (CSS) ---
st.set_page_config(layout="wide")

# CSS para un diseño limpio y profesional
css_profesional = """
    /* Fondo blanco para toda la app */
    .stApp {
        background-color: white;
    }

    /* Ocultar elementos innecesarios de Streamlit */
    .stApp > header, #MainMenu, footer {
        visibility: hidden;
    }

    /* Estilo profesional para el botón principal */
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
st.markdown(f"<style>{css_profesional}</style>", unsafe_allow_html=True)

# --- 2. MANEJO DE ESTADO DE SESIÓN (PARA NAVEGACIÓN) ---

# Inicializamos el estado si no existe.
# Esto nos dirá en qué "página" estamos.
if 'pagina_actual' not in st.session_state:
    st.session_state.pagina_actual = 'inicio'

# Funciones para cambiar de página
def ir_a_fase0():
    st.session_state.pagina_actual = 'fase0'

def ir_al_inicio():
    st.session_state.pagina_actual = 'inicio'


# --- 3. DEFINICIÓN DE LAS PÁGINAS ---

def pagina_inicio():
    """Renderiza la página de bienvenida."""
    _ , col2, _ = st.columns([1, 2, 1])

    with col2:
        # LOGO CENTRADO
        _ , logo_col, _ = st.columns([1, 1, 1])
        with logo_col:
            try:
                st.image('imagen.png', width=150)
            except Exception:
                st.warning("⚠️ No se encontró la imagen 'imagen.png'.")

        # TÍTULO Y DESCRIPCIÓN
        st.markdown("<h1 style='text-align: center; color: #1E3A5F;'>AUTOMATIZACIÓN DE MEMORIAS TÉCNICAS</h1>", unsafe_allow_html=True)
        st.write("")
        st.markdown("""
        <p style='text-align: center; font-size: 1.1em; color: #555;'>
            Esta herramienta está diseñada para simplificar y acelerar la creación de tus memorias técnicas.
            <br>
            Haz clic en <b>Comenzar</b> para iniciar el proceso.
        </p>
        """, unsafe_allow_html=True)
        st.write("")
        st.write("")

        # BOTÓN "COMENZAR"
        _ , btn_col, _ = st.columns([1, 1, 1])
        with btn_col:
            # Al hacer clic, se ejecutará la función para cambiar de página
            st.button("Comenzar", on_click=ir_a_fase0, use_container_width=True)


def pagina_fase0():
    """Renderiza la página para la Fase 0: Carga de documentos."""
    st.title("Fase 0: Preparación y Análisis")
    st.header("Sube aquí tus pliegos y plantilla para empezar el análisis")
    st.markdown("---")

    # TRADUCCIÓN DE LA LÓGICA DE COLAB A WIDGETS DE STREAMLIT

    # 1. Preguntar si hay plantilla
    tiene_plantilla = st.radio(
        "¿Dispones de una plantilla de memoria técnica?",
        ("Sí, voy a subir una", "No, generar estructura solo con los pliegos"),
        horizontal=True,
        label_visibility="collapsed" # Oculta la etiqueta para un look más limpio
    )

    plantilla_file = None
    if tiene_plantilla == "Sí, voy a subir una":
        plantilla_file = st.file_uploader(
            "📂 Sube tu plantilla (un único archivo DOCX o PDF)",
            type=['docx', 'pdf']
        )
    
    # 2. Pedir los pliegos (siempre)
    pliegos_files = st.file_uploader(
        "📂 Sube aquí el/los pliegos de la licitación (puedes seleccionar varios)",
        type=['docx', 'pdf'],
        accept_multiple_files=True
    )

    st.markdown("---")

    # 3. Botón para iniciar el análisis
    if st.button("Analizar Documentos", use_container_width=True):
        # Verificación de que los archivos necesarios están subidos
        if not pliegos_files:
            st.error("❌ Por favor, sube al menos un pliego para continuar.")
        elif tiene_plantilla == "Sí, voy a subir una" and not plantilla_file:
            st.error("❌ Has indicado que tienes una plantilla, por favor, súbela.")
        else:
            # Si todo está correcto, aquí conectaríamos tu lógica de análisis
            with st.spinner('Analizando documentos... Esto puede tardar unos minutos.'):
                # =================================================================
                # AQUÍ IRÍA LA LLAMADA A TUS FUNCIONES DE ANÁLISIS CON GEMINI
                # Por ahora, simulamos el proceso y mostramos los archivos subidos
                # =================================================================
                
                # Simulamos un tiempo de procesamiento
                time.sleep(3) 

                st.success("✅ ¡Análisis completado! (Simulación)")
                
                if plantilla_file:
                    st.write(f"**Plantilla recibida:** `{plantilla_file.name}`")
                
                st.write("**Pliegos recibidos:**")
                for pliego in pliegos_files:
                    st.write(f"- `{pliego.name}`")
                
                st.info("Siguiente paso: Mostrar la estructura generada para validación.")

    # Botón para volver al inicio
    st.button("Volver al Inicio", on_click=ir_al_inicio)


# --- 4. ROUTER PRINCIPAL DE LA APLICACIÓN ---
# Este bloque decide qué página mostrar basándose en el estado de la sesión.
if st.session_state.pagina_actual == 'inicio':
    pagina_inicio()
elif st.session_state.pagina_actual == 'fase0':
    pagina_fase0()
