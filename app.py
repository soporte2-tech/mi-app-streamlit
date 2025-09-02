import streamlit as st
import time
import google.generativeai as genai # <-- NUEVO
import json                        # <-- NUEVO
import re                          # <-- NUEVO
from pathlib import Path           # <-- NUEVO
from pypdf import PdfReader        # <-- NUEVO
import docx                        # <-- NUEVO

# --- 1. CONFIGURACIÓN DE LA PÁGINA Y ESTILOS (CSS) ---
st.set_page_config(layout="wide")

# (Tu CSS profesional se mantiene igual, lo omito por brevedad)
css_profesional = """
    /* ... Tu CSS aquí ... */
"""
st.markdown(f"<style>{css_profesional}</style>", unsafe_allow_html=True)


# --- 2. SECCIÓN DE PROMPTS Y FUNCIONES AUXILIARES (Traído de Colab) --- # <-- NUEVO

# ✅ PROMPTS PLANTILLAS
PROMPT_PLANTILLA = """
Eres un analista de documentos extremadamente preciso...
(Aquí va tu PROMPT_PLANTILLA completo)
"""
PROMPT_PLIEGOS = """
Eres un consultor experto en licitaciones y tu conocimiento se basa ÚNICAMENTE en los archivos que te he proporcionado...
(Aquí va tu PROMPT_PLIEGOS completo)
"""

def limpiar_respuesta_json(texto_sucio: str) -> str:
    """
    Limpia la respuesta de la IA para extraer un objeto JSON de forma robusta.
    """
    if not isinstance(texto_sucio, str):
        return ""

    match_bloque = re.search(r'```(?:json)?\s*(\{.*\})\s*```', texto_sucio, re.DOTALL)
    if match_bloque:
        return match_bloque.group(1).strip()

    match_objeto = re.search(r'\{.*\}', texto_sucio, re.DOTALL)
    if match_objeto:
        return match_objeto.group(0).strip()

    st.warning("No se pudo encontrar un JSON válido en la respuesta de la IA.")
    return ""

def extraer_texto_de_archivo(archivo_subido):
    """Extrae texto de un archivo subido (PDF o DOCX)."""
    texto_completo = ""
    try:
        if archivo_subido.name.endswith('.pdf'):
            reader = PdfReader(archivo_subido)
            for page in reader.pages:
                texto_completo += (page.extract_text() or "") + "\n"
        elif archivo_subido.name.endswith('.docx'):
            doc = docx.Document(archivo_subido)
            texto_completo = "\n".join([p.text for p in doc.paragraphs])
    except Exception as e:
        st.error(f"Error al leer el archivo '{archivo_subido.name}': {e}")
    return texto_completo

def mostrar_resultado_analisis(data):
    """Muestra la estructura y matices en formato Streamlit."""
    if not data:
        st.error("No se pudo generar el análisis.")
        return

    st.subheader("뼈 Estructura de Apartados Propuesta")
    for seccion in data.get("estructura_memoria", []):
        st.markdown(f"**{seccion.get('apartado', 'Sin Título')}**")
        with st.container():
            for sub in seccion.get("subapartados", []):
                st.markdown(f"&nbsp;&nbsp;&nbsp;&nbsp;- {sub}")

    st.subheader("📝 Matices e Indicaciones por Apartado")
    for matiz in data.get("matices_desarrollo", []):
        with st.expander(f"**{matiz.get('subapartado', 'Detalles')}**"):
            st.markdown(f"**Apartado principal:** {matiz.get('apartado', 'N/A')}")
            st.markdown(f"**Indicaciones:**")
            st.write(matiz.get('indicaciones', 'No hay indicaciones específicas.'))

# --- 3. MANEJO DE ESTADO DE SESIÓN ---

if 'pagina_actual' not in st.session_state:
    st.session_state.pagina_actual = 'inicio'
if 'analisis_resultado' not in st.session_state: # <-- NUEVO
    st.session_state.analisis_resultado = None

def ir_a_fase0():
    st.session_state.pagina_actual = 'fase0'
    st.session_state.analisis_resultado = None # Limpiar resultados al volver a empezar

def ir_al_inicio():
    st.session_state.pagina_actual = 'inicio'
    st.session_state.analisis_resultado = None # Limpiar resultados


# --- 4. DEFINICIÓN DE LAS PÁGINAS ---

def pagina_inicio():
    # ... Tu página de inicio se mantiene igual ...
    st.button("Comenzar", on_click=ir_a_fase0, use_container_width=True)


def pagina_fase0():
    """Renderiza la página para la Fase 0: Carga de documentos y ANÁLISIS REAL.""" # <-- MODIFICADO
    st.title("Fase 0: Preparación y Análisis")

    # Si no hay un análisis previo, mostramos la interfaz de subida
    if st.session_state.analisis_resultado is None:
        st.header("Sube aquí tus pliegos y plantilla para empezar el análisis")
        st.markdown("---")

        tiene_plantilla = st.radio(
            "¿Dispones de una plantilla de memoria técnica?",
            ("Sí, voy a subir una", "No, generar estructura solo con los pliegos"),
            horizontal=True,
            label_visibility="collapsed"
        )

        plantilla_file = None
        if tiene_plantilla == "Sí, voy a subir una":
            plantilla_file = st.file_uploader(
                "📂 Sube tu plantilla (un único archivo DOCX o PDF)",
                type=['docx', 'pdf']
            )

        pliegos_files = st.file_uploader(
            "📂 Sube aquí el/los pliegos de la licitación (puedes seleccionar varios)",
            type=['docx', 'pdf'],
            accept_multiple_files=True
        )

        st.markdown("---")

        if st.button("Analizar Documentos", use_container_width=True):
            if not pliegos_files:
                st.error("❌ Por favor, sube al menos un pliego para continuar.")
            elif tiene_plantilla == "Sí, voy a subir una" and not plantilla_file:
                st.error("❌ Has indicado que tienes una plantilla, por favor, súbela.")
            else:
                # =================================================================
                # AQUÍ EMPIEZA LA LÓGICA REAL DE ANÁLISIS CON GEMINI
                # =================================================================
                with st.spinner('Conectando con la IA y analizando documentos... Esto puede tardar varios minutos.'):
                    try:
                        # 1. Configurar API y Modelo
                        api_key = st.secrets["GEMINI_API_KEY"]
                        genai.configure(api_key=api_key)
                        model = genai.GenerativeModel('gemini-1.5-flash') # O el modelo que prefieras

                        # 2. Preparar contenido para la IA
                        prompt_a_usar = PROMPT_PLANTILLA if plantilla_file else PROMPT_PLIEGOS
                        contenido_ia = [prompt_a_usar]
                        texto_plantilla = ""

                        if plantilla_file:
                            st.info(f"Extrayendo texto de la plantilla: {plantilla_file.name}...")
                            texto_plantilla = extraer_texto_de_archivo(plantilla_file)
                            if texto_plantilla:
                                contenido_ia.append(texto_plantilla)

                        # 3. Subir pliegos a la API de Gemini
                        referencias_pliegos = []
                        for pliego in pliegos_files:
                            st.info(f"Subiendo pliego a la API: {pliego.name}...")
                            # La API necesita un archivo en disco, creamos uno temporal
                            temp_dir = Path("temp_files")
                            temp_dir.mkdir(exist_ok=True)
                            temp_path = temp_dir / pliego.name
                            temp_path.write_bytes(pliego.getvalue())

                            # Subimos el archivo y guardamos la referencia
                            referencia = genai.upload_file(path=temp_path, display_name=pliego.name)
                            referencias_pliegos.append(referencia)

                            # Limpiamos el archivo temporal
                            temp_path.unlink()

                        if referencias_pliegos:
                             contenido_ia.extend(referencias_pliegos)
                        
                        # 4. Llamar a la IA
                        st.info("Generando estructura... La IA está trabajando.")
                        generation_config = genai.GenerationConfig(response_mime_type="application/json")
                        response = model.generate_content(contenido_ia, generation_config=generation_config)

                        # 5. Procesar y guardar el resultado
                        if response and hasattr(response, 'text') and response.text:
                            json_limpio_str = limpiar_respuesta_json(response.text)
                            if json_limpio_str:
                                # Guardamos el resultado en el estado de sesión
                                st.session_state.analisis_resultado = json.loads(json_limpio_str)
                                st.success("✅ ¡Análisis completado!")
                                time.sleep(2) # Pausa para que el usuario lea el mensaje
                                st.rerun() # Volvemos a ejecutar el script para mostrar el resultado
                            else:
                                st.error("❌ La IA devolvió una respuesta, pero no se pudo extraer el JSON.")
                        else:
                            st.error(f"❌ La IA no generó una respuesta válida. Detalles: {response.prompt_feedback}")

                    except Exception as e:
                        st.error(f"Ocurrió un error inesperado durante el análisis: {e}")
                        st.stop()
    else:
        # Si ya tenemos un resultado, lo mostramos
        st.header("🔬 Resultado del Análisis")
        mostrar_resultado_analisis(st.session_state.analisis_resultado)
        st.markdown("---")
        # Aquí podrías añadir botones para validar, editar o generar el documento final

    # Botón para volver al inicio (siempre visible en esta página)
    st.button("Volver al Inicio", on_click=ir_al_inicio)


# --- 5. ROUTER PRINCIPAL DE LA APLICACIÓN ---
if st.session_state.pagina_actual == 'inicio':
    pagina_inicio()
elif st.session_state.pagina_actual == 'fase0':
    pagina_fase0()
