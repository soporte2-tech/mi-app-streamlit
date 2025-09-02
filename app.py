import streamlit as st
import time
import google.generativeai as genai
import json
import re
from pathlib import Path
from pypdf import PdfReader
import docx

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


# --- 2. SECCIÓN DE PROMPTS Y FUNCIONES AUXILIARES (Traído de Colab) ---

# ✅ PROMPTS (Pega aquí tus prompts completos para que no ocupen tanto espacio)
PROMPT_PLANTILLA = """
Eres un analista de documentos extremadamente preciso.
Te daré el texto de una plantilla de memoria técnica y los Pliegos correspondientes.
Tu única tarea es convertirlo a un objeto JSON que contenga la estructura del indice y unas indicaciones para que la persona
que va a redactar la memoria técnica sepa todo lo necesario para poder redactar la memoria técnica con mayor puntuación.

## REGLAS ESTRICTAS:
1.  La estructura del documento debes sacarlo de la plantilla y las indicaciones mezclando esa información con la de los pliegos.
2.  El objeto JSON DEBE contener dos claves de nivel superior y solo dos: "estructura_memoria" y "matices_desarrollo".
3.  Para CADA apartado y subapartado, DEBES anteponer su numeración correspondiente (ej: "1. Título", "1.1. Subtítulo").
    ESTO ES OBLIGATORIO Y DEBE SER EN NÚMEROS NORMALES (1,2,3...) NADA DE LETRAS NI COSAS RARAS.
4.  La clave "estructura_memoria" contiene la lista de apartados y subapartados como un ÍNDICE.
    La lista "subapartados" SOLO debe contener los TÍTULOS numerados, NUNCA el texto de las instrucciones.
5.  Debes coger exactamente el mismo título del apartado o subapartado que existe en el texto de la plantilla, no lo modifiques.
    Mantenlo aunque esté en otro idioma.
6.  La clave "matices_desarrollo" desglosa CADA subapartado, asociando su título numerado con las INSTRUCCIONES completas.
    NO RESUMAS. DEBES CONTAR TODO LO QUE SEPAS DE ELLO.
    Llena estas indicaciones de mucho contexto útil para que alguien sin experiencia pueda redactar la memoria.
7.  DEBES INDICAR OBLIGATORIAMENTE LA LONGITUD DE CADA SUBAPARTADO.
    NO TE LO PUEDES INVENTAR. ESTE DATO ES CLAVE.
8.  Cada instrucción debe incluir. Si no tiene eso la instrucción no vale:
    - La longitud exacta de palabras del apartado (o aproximada según lo que se diga en los pliegos). No pongas en ningún caso
    "La longitud de este subapartado no está especificada en los documentos proporcionados", propon tú uno si no existe. Esta proposición debe
    ser coherente con el apartado que es y con lo que se valora en los pliegos.
    - Una explicación clara de lo que incluirá este apartado.
    - El objetivo de contenido para que este apartado sume a obtener la excelencia en la memoria técnica.
    - Cosas que no deben faltar en el apartado.

## MEJORAS AÑADIDAS:
- Responde SIEMPRE en formato JSON válido y bien estructurado. No incluyas texto fuera del objeto JSON.
- No inventes información: solo utiliza lo que aparezca en la plantilla o en los pliegos.
- Debes mostrar conocimiento de los pliegos, no puedes asumir que el que lee las intrucciones ya posee ese conociminento.
Debes explicar todo como si el que fuera a leer las indicaciones no supiera nada del tema y deba redactar todo el contenido.
- Mantén consistencia en la numeración (ejemplo: 1, 1.1, 1.1.1). Nunca mezcles números y letras.
- Si los pliegos mencionan tablas, gráficos o anexos obligatorios, añádelos en las indicaciones como recordatorio.
- Si hay discrepancias entre plantilla y pliego, PRIORIZA SIEMPRE lo que diga el pliego.
- Valida que cada subapartado en "estructura_memoria" tenga su correspondiente bloque en "matices_desarrollo".

## EJEMPLO DE ESTRUCTURA DE SALIDA OBLIGATORIA:
{
  "estructura_memoria": [
    {
      "apartado": "1. Análisis",
      "subapartados": ["1.1. Contexto", "1.2. DAFO"]
    }
  ],
  "matices_desarrollo": [
    {
      "apartado": "1. Análisis",
      "subapartado": "1.1. Contexto",
      "indicaciones": "El subapartado debe durar 5 páginas. Este subapartado debe describir el objeto de la contratación, que es la prestación de servicios de asesoramiento, mentoría y consultoría a personas emprendedoras autónomas en Galicia. El objetivo principal es apoyar la consolidación y crecimiento de 200 proyectos empresariales de trabajadores autónomos, a través de una red de mentores especializados, para potenciar sus competencias emprendedoras, mejorar su competitividad y reducir los riesgos. Se espera que se incluyan las dos modalidades de consultoría y mentoring: una estratégica para mejorar rendimiento y rentabilidad, y otra especializada para el desarrollo de una estrategia de expansión y escalabilidad, incluyendo un análisis competitivo y de mercado..."
    },
    {
      "apartado": "1. Análisis",
      "subapartado": "1.2. DAFO",
      "indicaciones": "El subapartado debe durar 5 páginas. Este subapartado debe conseguir mostrar ..."
    }
  ]
}
"""
PROMPT_PLIEGOS = """
Eres un consultor experto en licitaciones y tu conocimiento se basa ÚNICAMENTE en los archivos que te he proporcionado.
Tu misión es analizar los Pliegos y proponer una estructura para la memoria técnica que responda a todos los requisitos y criterios de valoración.
Te daré los pliegos para hacer la memoria técnica. Revisa cuidadosamente todos los que te mando (técnicos y administrativos) para sacar la estructura obligatoria, mínima o recomendada.
Tu única tarea es convertirlo a un objeto JSON que contenga la estructura del indice y unas indicaciones para que la persona
que va a redactar la memoria técnica sepa todo lo necesario para poder redactar la memoria técnica con mayor puntuación.

## REGLAS ESTRICTAS:
1.  Tu respuesta DEBE ser un único objeto JSON válido y nada más. Sin texto introductorio ni marcadores de formato como ```json.
2.  El objeto JSON DEBE contener dos claves de nivel superior y solo dos: "estructura_memoria" y "matices_desarrollo".
3.  Para CADA apartado y subapartado, DEBES anteponer su numeración correspondiente (ej: "1. Título", "1.1. Subtítulo").
    ESTO ES OBLIGATORIO Y DEBE SER EN NÚMEROS NORMALES (1,2,3...) NADA DE LETRAS NI COSAS RARAS.
4.  La clave "estructura_memoria" contiene la lista de apartados y subapartados como un ÍNDICE.
    La lista "subapartados" SOLO debe contener los TÍTULOS numerados, NUNCA el texto de las instrucciones.
5.  Debes coger exactamente el mismo título del apartado o subapartado que existe en los Pliegos, no lo modifiques.
    Mantenlo aunque esté en otro idioma.
6.  La clave "matices_desarrollo" desglosa CADA subapartado, asociando su título numerado con las INSTRUCCIONES completas.
    NO RESUMAS. DEBES CONTAR TODO LO QUE SEPAS DE ELLO.
    Llena estas indicaciones de mucho contexto útil para que alguien sin experiencia pueda redactar la memoria.
7.  DEBES INDICAR OBLIGATORIAMENTE LA LONGITUD DE CADA SUBAPARTADO.
    NO TE LO PUEDES INVENTAR. ESTE DATO ES CLAVE.
8.  Cada instrucción debe incluir. Si no tiene eso la instrucción no vale:
    - La longitud exacta de palabras del apartado (o aproximada según lo que se diga en los Pliegos).
      No pongas en ningún caso "La longitud de este subapartado no está especificada en los documentos proporcionados";
      propone tú una si no existe. Esta proposición debe ser coherente con el apartado que es y con lo que se valora en los Pliegos.
    - Una explicación clara de lo que incluirá este apartado.
    - El objetivo de contenido para que este apartado sume a obtener la excelencia en la memoria técnica.
    - Cosas que no deben faltar en el apartado.

## MEJORAS AÑADIDAS:
- Responde SIEMPRE en formato JSON válido y bien estructurado. No incluyas texto fuera del objeto JSON.
- No inventes información: utiliza únicamente lo que aparezca en los Pliegos.
- Debes mostrar conocimiento de los Pliegos; no puedes asumir que quien lea las indicaciones ya posee ese conocimiento.
  Explica todo como si la persona que redacta no supiera nada del tema y necesitara todas las claves para escribir el contenido.
- Mantén consistencia en la numeración (ejemplo: 1, 1.1, 1.1.1). Nunca mezcles números y letras.
- Si los Pliegos mencionan tablas, gráficos o anexos obligatorios, añádelos en las indicaciones como recordatorio.
- Valida que cada subapartado en "estructura_memoria" tenga su correspondiente bloque en "matices_desarrollo".

## EJEMPLO DE ESTRUCTURA DE SALIDA OBLIGATORIA:
{
  "estructura_memoria": [
    {
      "apartado": "1. Solución Técnica",
      "subapartados": ["1.1. Metodología", "1.2. Plan de Trabajo"]
    }
  ],
  "matices_desarrollo": [
    {
      "apartado": "1. Solución Técnica",
      "subapartado": "1.1. Metodología",
      "indicaciones": "El subapartado debe durar 5 páginas. Este subapartado debe describir el objeto de la contratación, que es la prestación de servicios de asesoramiento, mentoría y consultoría a personas emprendedoras autónomas en Galicia. El objetivo principal es apoyar la consolidación y crecimiento de 200 proyectos empresariales de trabajadores autónomos, a través de una red de mentores especializados, para potenciar sus competencias emprendedoras, mejorar su competitividad y reducir los riesgos. Se espera que se incluyan las dos modalidades de consultoría y mentoring: una estratégica para mejorar rendimiento y rentabilidad, y otra especializada para el desarrollo de una estrategia de expansión y escalabilidad, incluyendo un análisis competitivo y de mercado..."
    },
    {
      "apartado": "1. Solución Técnica",
      "subapartado": "1.2. Plan de Trabajo",
      "indicaciones": "El subapartado debe durar 5 páginas. Este subapartado debe conseguir mostrar ..."
    }
  ]
}
"""

def limpiar_respuesta_json(texto_sucio: str) -> str:
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
if 'analisis_resultado' not in st.session_state:
    st.session_state.analisis_resultado = None

def ir_a_fase0():
    st.session_state.pagina_actual = 'fase0'
    st.session_state.analisis_resultado = None

def ir_al_inicio():
    st.session_state.pagina_actual = 'inicio'
    st.session_state.analisis_resultado = None

# --- 4. DEFINICIÓN DE LAS PÁGINAS ---

def pagina_inicio():
    """Renderiza la página de bienvenida. (VERSIÓN ORIGINAL RESTAURADA)"""
    _ , col2, _ = st.columns([1, 2, 1])

    with col2:
        # LOGO CENTRADO
        _ , logo_col, _ = st.columns([1, 1, 1])
        with logo_col:
            try:
                # Asegúrate de tener un archivo 'imagen.png' en la misma carpeta que tu script
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
            st.button("Comenzar", on_click=ir_a_fase0, use_container_width=True)


def pagina_fase0():
    """Renderiza la página para la Fase 0: Carga de documentos y ANÁLISIS REAL."""
    st.title("Fase 0: Preparación y Análisis")

    if st.session_state.analisis_resultado is None:
        st.header("Sube aquí tus pliegos y plantilla para empezar el análisis")
        st.markdown("---")

        # ... (La parte de subir archivos se mantiene igual) ...
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
                with st.spinner('Conectando con la IA y analizando documentos... Esto puede tardar varios minutos.'):
                    try:
                        api_key = st.secrets["GEMINI_API_KEY"]
                        genai.configure(api_key=api_key)
                        
                        # --- INICIO DE CAMBIOS ---
                        # Opción 1: Usar el modelo Pro
                        model = genai.GenerativeModel('gemini-1.5-pro') 
                        # --- FIN DE CAMBIOS ---

                        prompt_a_usar = PROMPT_PLANTILLA if plantilla_file else PROMPT_PLIEGOS
                        contenido_ia = [prompt_a_usar]
                        
                        if plantilla_file:
                            st.info(f"Extrayendo texto de la plantilla: {plantilla_file.name}...")
                            texto_plantilla = extraer_texto_de_archivo(plantilla_file)
                            if texto_plantilla:
                                contenido_ia.append(texto_plantilla)

                        referencias_pliegos = []
                        temp_dir = Path("temp_files")
                        temp_dir.mkdir(exist_ok=True)
                        for pliego in pliegos_files:
                            st.info(f"Subiendo pliego a la API: {pliego.name}...")
                            temp_path = temp_dir / pliego.name
                            with open(temp_path, "wb") as f:
                                f.write(pliego.getvalue())
                            
                            referencia = genai.upload_file(path=temp_path, display_name=pliego.name)
                            referencias_pliegos.append(referencia)
                            temp_path.unlink()

                        if referencias_pliegos:
                             contenido_ia.extend(referencias_pliegos)
                        
                        st.info("Generando estructura... La IA está trabajando. Este proceso es largo, por favor ten paciencia.")
                        
                        # --- INICIO DE CAMBIOS ---
                        # Opción 2: Permitir más tokens de salida
                        generation_config = genai.GenerationConfig(
                            response_mime_type="application/json",
                            max_output_tokens=8192 
                        )
                        # --- FIN DE CAMBIOS ---

                        response = model.generate_content(contenido_ia, generation_config=generation_config)

                        if response and hasattr(response, 'text') and response.text:
                            json_limpio_str = limpiar_respuesta_json(response.text)
                            if json_limpio_str:
                                st.session_state.analisis_resultado = json.loads(json_limpio_str)
                                st.success("✅ ¡Análisis completado!")
                                time.sleep(2)
                                st.rerun()
                            else:
                                st.error("❌ La IA devolvió una respuesta, pero no se pudo extraer el JSON. Posiblemente la respuesta estaba incompleta.")
                        else:
                            st.error(f"❌ La IA no generó una respuesta válida. Detalles: {response.prompt_feedback}")

                    except Exception as e:
                        st.error(f"Ocurrió un error inesperado durante el análisis: {e}")
    else:
        st.header("🔬 Resultado del Análisis")
        mostrar_resultado_analisis(st.session_state.analisis_resultado)
        st.markdown("---")

    st.button("Volver al Inicio", on_click=ir_al_inicio)


# --- 5. ROUTER PRINCIPAL DE LA APLICACIÓN ---
if st.session_state.pagina_actual == 'inicio':
    pagina_inicio()
elif st.session_state.pagina_actual == 'fase0':
    pagina_fase0()
