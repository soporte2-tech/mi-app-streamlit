import streamlit as st
from PIL import Image

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
    }

    .stApp {
        background-color: #f0f2f6;
    }

    .stApp > header {
        background-color: #ffffff;
        padding: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        border-radius: 10px;
        margin-bottom: 20px;
    }

    .title-container {
        display: flex;
        align-items: center;
        gap: 20px;
        padding: 20px;
    }

    .logo-img {
        border-radius: 8px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }

    .st-emotion-cache-1jmveo6 {
        display: flex;
        align-items: center;
        justify-content: center;
    }
"""

st.markdown(f"<style>{css_content}</style>", unsafe_allow_html=True)

# --- CABECERA CON LOGO Y TÍTULO ---
st.markdown("""
<div class="title-container">
    <div style="flex-grow: 1;">
        <h1 style="color: #004d99; font-weight: 700; font-size: 2.5em;">AUTOMATIZACIÓN DE MEMORIAS TÉCNICAS</h1>
    </div>
    <div>
        <!-- Usaremos el logo de ejemplo hasta que el usuario suba el suyo -->
        <img src="https://placehold.co/150x75/004d99/ffffff?text=DPI+Estrategia" alt="Logo de la empresa" class="logo-img">
    </div>
</div>
<hr style="border: 2px solid #004d99; margin: 20px 0;">
""", unsafe_allow_html=True)

# --- CONTENIDO DE LA PÁGINA ---
# Este es un diseño profesional y limpio.
st.subheader("¡Bienvenido al asistente de memorias técnicas!")
st.write("Esta herramienta está diseñada para simplificar y acelerar la creación de tus memorias técnicas. Usa el menú lateral para navegar por las diferentes funcionalidades.")

st.info("💡 **Consejo:** Una vez que subas el archivo `imagen.png` a GitHub, el logo de ejemplo se reemplazará automáticamente.")

st.markdown("---")

st.markdown("""
### ¿Qué puedes esperar?
- **Agilidad**: Reduce el tiempo de redacción de documentos complejos.
- **Precisión**: Genera contenido basado en datos y directrices predefinidas.
- **Colaboración**: Permite un flujo de trabajo más eficiente con tu equipo.
""")
