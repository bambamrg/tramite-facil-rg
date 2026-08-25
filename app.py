import streamlit as st
import json

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


# ============================================================
# CONFIGURACIÓN
# ============================================================

st.set_page_config(
    page_title="Trámite Fácil",
    page_icon="🏛️",
    layout="centered"
)


# ============================================================
# ACCESIBILIDAD Y PREFERENCIAS VISUALES
# ============================================================

# Inicializar preferencias

if "modo_oscuro" not in st.session_state:
    st.session_state.modo_oscuro = False

if "tamano_texto" not in st.session_state:
    st.session_state.tamano_texto = "Normal"




# Tamaños según la preferencia

tamanos_texto = {
    "Normal": {
        "texto": "18px",
        "titulo": "32px",
        "subtitulo": "24px",
        "icono": "28px"
    },
    "Grande": {
        "texto": "21px",
        "titulo": "38px",
        "subtitulo": "28px",
        "icono": "34px"
    },
    "Muy grande": {
        "texto": "24px",
        "titulo": "44px",
        "subtitulo": "32px",
        "icono": "40px"
    }
}

config_visual = tamanos_texto[
    st.session_state.tamano_texto
]


# Colores según el tema

if st.session_state.modo_oscuro:

    color_fondo = "#121212"
    color_texto = "#F5F5F5"
    color_secundario = "#1E1E1E"
    color_borde = "#444444"

else:

    color_fondo = "#FFFFFF"
    color_texto = "#1A1A1A"
    color_secundario = "#F5F7FA"
    color_borde = "#D9D9D9"


# Aplicar estilos dinámicos

st.markdown(
    f"""
    <style>

    .stApp {{
        background-color: {color_fondo};
        color: {color_texto};
    }}

    p, li, label, div {{
        font-size: {config_visual["texto"]};
    }}

    h1 {{
        font-size: {config_visual["titulo"]} !important;
    }}

    h2, h3 {{
        font-size: {config_visual["subtitulo"]} !important;
    }}

    button {{
        font-size: {config_visual["texto"]} !important;
    }}

    .stButton button {{
    min-height: 48px;
    width: 100%;
    color: {color_texto} !important;
    background-color: {color_secundario} !important;
    border: 1px solid {color_borde} !important;
    border-radius: 10px !important;
    font-size: {config_visual["texto"]} !important;
    font-weight: 600 !important;
}}

.stButton button:hover {{
    color: {color_texto} !important;
    border-color: {color_texto} !important;
}}

        .hero {{
        background-color: {color_secundario};
        border: 1px solid {color_borde};
        border-radius: 18px;
        padding: 35px 25px;
        text-align: left;
        margin-bottom: 20px;
    }}

    .hero-icon {{
        font-size: {config_visual["icono"]};
        margin-bottom: 10px;
    }}

    .hero-title {{
        font-size: {config_visual["titulo"]} !important;
        font-weight: 700;
        margin-bottom: 10px;
    }}

    .hero-subtitle {{
        font-size: {config_visual["texto"]} !important;
        opacity: 0.8;
        margin: 0 auto;
        max-width: 650px;
    }}

    .accessibility-title {{
        font-size: {config_visual["texto"]};
        font-weight: 700;
        margin-bottom: 8px;
    }}

    .tramite-card-description {{
        font-size: {config_visual["texto"]};
        opacity: 0.75;
        margin-top: 8px;
        line-height: 1.35;
    }}

    .search-card {{
         background-color: {color_secundario};
         border: 2px solid {color_borde};
         border-radius: 18px;
         padding: 28px;
         margin-top: 22px;
         margin-bottom: 10px;
     }}

     .search-eyebrow {{
         font-size: 0.85em;
         font-weight: 700;
         letter-spacing: 0.08em;
         text-transform: uppercase;
         margin-bottom: 6px;
         opacity: 0.75;
     }}

     .search-card h2 {{
         margin-top: 0;
         margin-bottom: 8px;
     }}

     .search-description {{
         font-size: {config_visual["texto"]};
         opacity: 0.85;
         margin-bottom: 4px;
         line-height: 1.45;
     }}

     div[data-testid="stTextInput"] input {{
         min-height: 56px;
         font-size: {config_visual["texto"]} !important;
         padding: 12px 16px !important;
         border-width: 2px !important;
         border-radius: 12px !important;
     }}

     div[data-testid="stTextInput"] label {{
         font-weight: 700 !important;
         margin-bottom: 6px !important;
     }}

     div[data-testid="stRadio"] label {{
         font-weight: 600 !important;
     }}

     div[data-testid="stRadio"] div[role="radiogroup"] {{
         gap: 8px;
     }}
     .quick-access-title {{
        text-align: center;
        font-size: {config_visual["subtitulo"]} !important;
        font-weight: 600;
        margin-top: 20px;
        margin-bottom: 20px;
    }}

    .quick-access-description {{
        text-align: center;
        font-size: {config_visual["texto"]};
        opacity: 0.8;
        margin-bottom: 20px;
    }}

    .tramite-card {{
        background-color: {color_secundario};
        border: 1px solid {color_borde};
        border-radius: 16px;
        padding: 20px 10px;
        text-align: center;
        min-height: 150px;
    }}

    .tramite-card-icon {{
        font-size: {config_visual["icono"]};
        margin-bottom: 10px;
    }}

    .tramite-card-title {{
        font-size: {config_visual["texto"]};
        font-weight: 600;
    }}

    .tramite-header {{
    display: flex;
    align-items: center;
    gap: 18px;
    background-color: {color_secundario};
    border: 1px solid {color_borde};
    border-radius: 18px;
    padding: 25px;
    margin-top: 25px;
    margin-bottom: 25px;
}}

.tramite-header-icon {{
    font-size: {config_visual["icono"]};
    min-width: 55px;
    text-align: center;
}}

.tramite-header-content {{
    flex: 1;
}}

.tramite-header-title {{
    font-size: {config_visual["subtitulo"]} !important;
    font-weight: 700;
    color: {color_texto} !important;
}}

.tramite-header-description {{
    font-size: {config_visual["texto"]} !important;
    color: {color_texto} !important;
    opacity: 0.8;
    margin-top: 5px;
}}

    .tramite-header-icon {{
        font-size: {config_visual["icono"]};
        min-width: 50px;
        text-align: center;
    }}

    .tramite-header-title {{
        font-size: {config_visual["subtitulo"]} !important;
        font-weight: 700;
    }}

    .tramite-header-description {{
        font-size: {config_visual["texto"]};
        opacity: 0.8;
        margin-top: 5px;
    }}

        .streamlit-expanderHeader {{
        font-size: {config_visual["texto"]} !important;
        font-weight: 600;
    }}

    .streamlit-expanderContent {{
        font-size: {config_visual["texto"]} !important;
    }}

        .stSelectbox label {{
        color: {color_texto} !important;
        font-size: {config_visual["texto"]} !important;
        font-weight: 600 !important;
    }}

    .stSelectbox div[data-baseweb="select"] {{
        font-size: {config_visual["texto"]} !important;
    }}

    
    /* Mejoras de accesibilidad visual y teclado */
    .stButton button:focus-visible,
    input:focus-visible,
    textarea:focus-visible,
    select:focus-visible,
    [role="button"]:focus-visible {{
        outline: 3px solid #FFD54F !important;
        outline-offset: 3px !important;
        box-shadow: 0 0 0 2px #111111 !important;
    }}

    .tramite-card {{
        min-height: 170px;
    }}

    .tramite-card-description,
    .search-description,
    .quick-access-description,
    .hero-subtitle {{
        line-height: 1.6 !important;
    }}

    /* No depender únicamente del color para indicar estados */
    .stButton button {{
        text-decoration: none !important;
    }}

    @media (max-width: 640px) {{
        .tramite-card {{
            min-height: auto;
        }}
    }}

    </style>
    """,
    unsafe_allow_html=True
)

# ============================================================
# CARGAR DATOS
# ============================================================

def cargar_datos():

    with open(
        "data/tramites.json",
        "r",
        encoding="utf-8"
    ) as archivo:

        return json.load(archivo)


datos = cargar_datos()


# ============================================================
# CREAR DOCUMENTOS PARA TF-IDF DE LAS SECCIONES
# ============================================================

def crear_documentos_secciones(tramites):

    documentos = []

    for tramite in tramites:

        for seccion in tramite["secciones"]:

            texto = (
                tramite["nombre"]
                + " "
                + seccion["titulo"]
                + " "
            )

            for bloque in seccion["bloques"]:

                if "contenido" in bloque:

                    texto += (
                        str(bloque["contenido"])
                        + " "
                    )

                if "elementos" in bloque:

                    texto += (
                        " ".join(
                            str(elemento)
                            for elemento in bloque["elementos"]
                        )
                        + " "
                    )

            documentos.append(
                {
                    "tramite": tramite["nombre"],
                    "seccion": seccion["titulo"],
                    "texto": texto
                }
            )

    return documentos


documentos_secciones = crear_documentos_secciones(
    datos["tramites"]
)


# ============================================================
# CREAR DOCUMENTOS PARA TF-IDF DE LOS TRÁMITES
# ============================================================

def crear_documentos_tramites(tramites):

    documentos = []

    for tramite in tramites:

        texto = (
            tramite["nombre"]
            + " "
            + tramite["descripcion"]
            + " "
        )

        for seccion in tramite["secciones"]:

            texto += (
                seccion["titulo"]
                + " "
            )

            for bloque in seccion["bloques"]:

                if "contenido" in bloque:

                    texto += (
                        str(bloque["contenido"])
                        + " "
                    )

                if "elementos" in bloque:

                    texto += (
                        " ".join(
                            str(elemento)
                            for elemento in bloque["elementos"]
                        )
                        + " "
                    )

        documentos.append(
            {
                "tramite": tramite["nombre"],
                "texto": texto
            }
        )

    return documentos


documentos_tramites = crear_documentos_tramites(
    datos["tramites"]
)


# ============================================================
# DETECTAR TRÁMITE CON REGLAS
# ============================================================

def detectar_tramite(consulta, tramites):

    consulta = consulta.lower().strip()

    # --------------------------------------------------------
    # ESTACIONAMIENTO MEDIDO
    # --------------------------------------------------------

    palabras_estacionamiento = [
        "estacionamiento",
        "estacionar",
        "estacionado",
        "parking",
        "sem",
        "estacionamiento medido",
        "estacionamiento tarifado",
        "zona tarifada",
        "zona de estacionamiento",
        "pagar estacionamiento",
        "pago del estacionamiento",
        "multa de estacionamiento"
    ]

    # --------------------------------------------------------
    # LICENCIA DE CONDUCIR
    # --------------------------------------------------------

    palabras_licencia = [
        "licencia",
        "registro",
        "conducir",
        "manejar",
        "manejo",
        "carnet",
        "carné",
        "permiso para conducir",
        "permiso para manejar",
        "licencia de conducir",
        "sacar el registro",
        "sacar mi registro",
        "renovar mi registro",
        "renovar licencia",
        "examen de manejo",
        "examen práctico",
        "examen practico",
        "examen teórico",
        "examen teorico"
    ]

    # --------------------------------------------------------
    # APROBACIÓN DE PLANOS
    # --------------------------------------------------------

    palabras_planos = [
        "plano",
        "planos",
        "construccion",
        "construcción",
        "construir",
        "construyo",
        "obra",
        "obras",
        "edificar",
        "edificación",
        "arquitecto",
        "arquitecta",
        "ingeniero",
        "ingeniera",
        "maestro mayor",
        "casa",
        "papeles para construir",
        "documentación para construir",
        "documentacion para construir",
        "expediente",
        "expediente final",
        "carpeta técnica",
        "carpeta tecnica",
        "carpeta técnica previa",
        "carpeta tecnica previa",
        "planos finales",
        "documentación de obra",
        "documentacion de obra",
        "documentos de obra",
        "papeles de obra",
        "inicio de obra",
        "certificado de inicio de obra",
        "obra terminada",
        "obra finalizada",
        "finalizar la obra",
        "finalizar obra",
        "aprobar planos",
        "aprobación de planos",
        "aprobacion de planos",
        "obras particulares"
    ]

    puntajes = {
        "Estacionamiento Medido": 0,
        "Licencia de Conducir": 0,
        "Aprobación de Planos": 0
    }

    for palabra in palabras_estacionamiento:

        if palabra in consulta:
            puntajes["Estacionamiento Medido"] += 1

    for palabra in palabras_licencia:

        if palabra in consulta:
            puntajes["Licencia de Conducir"] += 1

    for palabra in palabras_planos:

        if palabra in consulta:
            puntajes["Aprobación de Planos"] += 1

    tramite_detectado = max(
        puntajes,
        key=puntajes.get
    )

    if puntajes[tramite_detectado] == 0:
        return None

    for tramite in tramites:

        if tramite["nombre"] == tramite_detectado:
            return tramite

    return None


# ============================================================
# BUSCAR TRÁMITE POR SIMILITUD TF-IDF
# ============================================================

def buscar_tramite_por_similitud(
    consulta,
    cantidad_resultados=1
):

    if not documentos_tramites:
        return []

    textos = [
        documento["texto"]
        for documento in documentos_tramites
    ]

    vectorizador = TfidfVectorizer()

    matriz = vectorizador.fit_transform(
        textos + [consulta]
    )

    vector_consulta = matriz[-1]
    vectores_documentos = matriz[:-1]

    similitudes = cosine_similarity(
        vector_consulta,
        vectores_documentos
    ).flatten()

    indices_ordenados = similitudes.argsort()[::-1]

    resultados = []

    for indice in indices_ordenados[
        :cantidad_resultados
    ]:

        resultados.append(
            {
                "nombre": documentos_tramites[indice]["tramite"],
                "similitud": similitudes[indice]
            }
        )

    return resultados


# ============================================================
# DETECTAR INTENCIÓN / SECCIONES
# ============================================================

def detectar_secciones(consulta, tramite):

    consulta = consulta.lower().strip()

    secciones_detectadas = []


    # ========================================================
    # ESTACIONAMIENTO MEDIDO
    # ========================================================

    if tramite["nombre"] == "Estacionamiento Medido":

        palabras_como_funciona = [
            "cómo funciona",
            "como funciona",
            "cómo se usa",
            "como se usa",
            "cómo funciona el estacionamiento",
            "como funciona el estacionamiento",
            "cómo funciona el sem",
            "como funciona el sem"
        ]

        palabras_formas_pago = [
            "pagar",
            "pago",
            "forma de pago",
            "formas de pago",
            "cómo pago",
            "como pago",
            "pagar con app",
            "aplicación",
            "aplicacion",
            "app",
            "sem río grande",
            "sem rio grande"
        ]

        palabras_puntos_venta = [
            "punto de venta",
            "puntos de venta",
            "dónde compro",
            "donde compro",
            "dónde puedo comprar",
            "donde puedo comprar",
            "comercio",
            "comercios",
            "kiosco",
            "kioscos"
        ]

        palabras_tarifas = [
            "tarifa",
            "tarifas",
            "precio",
            "precios",
            "cuánto cuesta",
            "cuanto cuesta",
            "cuánto pago",
            "cuanto pago",
            "hora",
            "horas",
            "15 minutos",
            "quince minutos",
            "tiempo"
        ]

        palabras_excepciones = [
            "excepción",
            "excepcion",
            "excepciones",
            "no pagar",
            "no tengo que pagar",
            "no tienen que pagar",
            "no debe pagar",
            "no deben pagar",
            "exento",
            "exenta",
            "frentista",
            "discapacidad",
            "discapacitado",
            "taxi",
            "remis",
            "ambulancia",
            "bombero",
            "policía",
            "policia"
        ]

        palabras_infracciones = [
            "infracción",
            "infraccion",
            "infracciones",
            "multa",
            "multas",
            "no pagué",
            "no pague",
            "no pago",
            "si no pago",
            "qué pasa si no pago",
            "que pasa si no pago",
            "incumplimiento"
        ]

        # Prioridad: infracciones y excepciones antes que pago.

        es_infraccion = any(
            palabra in consulta
            for palabra in palabras_infracciones
        )

        es_excepcion = any(
            palabra in consulta
            for palabra in palabras_excepciones
        )

        if es_infraccion:

            secciones_detectadas.append(
                {"nombre": "Infracciones"}
            )

        elif es_excepcion:

            secciones_detectadas.append(
                {"nombre": "Excepciones al pago"}
            )

        elif any(
            palabra in consulta
            for palabra in palabras_formas_pago
        ):

            secciones_detectadas.append(
                {"nombre": "Formas de pago"}
            )

        if any(
            palabra in consulta
            for palabra in palabras_puntos_venta
        ):

            secciones_detectadas.append(
                {"nombre": "Puntos de venta"}
            )

        if any(
            palabra in consulta
            for palabra in palabras_tarifas
        ):

            secciones_detectadas.append(
                {"nombre": "Tarifas y tiempos"}
            )

        if any(
            palabra in consulta
            for palabra in palabras_como_funciona
        ):

            secciones_detectadas.append(
                {"nombre": "Cómo funciona"}
            )


    # ========================================================
    # LICENCIA DE CONDUCIR
    # ========================================================

    elif tramite["nombre"] == "Licencia de Conducir":

        palabras_primera_vez = [
            "primera vez",
            "sacar mi licencia",
            "sacar la licencia",
            "obtener licencia",
            "obtener mi licencia",
            "sacar el registro",
            "sacar mi registro",
            "quiero manejar",
            "quiero conducir",
            "obtener permiso"
        ]

        palabras_renovacion = [
            "renovar",
            "renovación",
            "renovacion",
            "vencida",
            "vencido",
            "vence",
            "vencimiento",
            "mi licencia venció",
            "mi licencia vencio"
        ]

        palabras_menores = [
            "17 años",
            "diecisiete años",
            "menor",
            "menores",
            "menor de edad",
            "autorización",
            "autorizacion"
        ]

        palabras_profesionales = [
            "profesional",
            "profesionales",
            "clase c",
            "clase d",
            "clase e",
            "camión",
            "camion",
            "colectivo"
        ]

        palabras_lugares = [
            "dónde",
            "donde",
            "dirección",
            "direccion",
            "lugar",
            "lugares",
            "cgp",
            "cgp padre zink",
            "padre zink",
            "laserre",
            "kartódromo",
            "kartodromo",
            "pellegrini",
            "viedma"
        ]

        if any(
            palabra in consulta
            for palabra in palabras_primera_vez
        ):

            secciones_detectadas.append(
                {"nombre": "Licencia por primera vez"}
            )

        if any(
            palabra in consulta
            for palabra in palabras_renovacion
        ):

            secciones_detectadas.append(
                {"nombre": "Renovación"}
            )

        if any(
            palabra in consulta
            for palabra in palabras_menores
        ):

            secciones_detectadas.append(
                {"nombre": "Menores de edad"}
            )

        if any(
            palabra in consulta
            for palabra in palabras_profesionales
        ):

            secciones_detectadas.append(
                {"nombre": "Conductores profesionales"}
            )

        if any(
            palabra in consulta
            for palabra in palabras_lugares
        ):

            secciones_detectadas.append(
                {
                    "nombre":
                    "Lugares relacionados con el trámite"
                }
            )


    # ========================================================
    # APROBACIÓN DE PLANOS
    # ========================================================

    elif tramite["nombre"] == "Aprobación de Planos":

        palabras_documentacion_final = [
            "documentacion final",
            "documentación final",
            "documentos finales",
            "papeles finales",
            "planos finales",
            "expediente final",
            "al finalizar",
            "al final",
            "para finalizar",
            "finalizar el tramite",
            "finalizar el trámite",
            "terminar el tramite",
            "terminar el trámite",
            "termine",
            "terminé",
            "ya termine",
            "ya terminé",
            "terminada",
            "terminado",
            "una vez terminado",
            "despues de terminar",
            "después de terminar",
            "ultima etapa",
            "última etapa",
            "etapa final"
        ]

        palabras_documentacion_inicial = [
            "documentacion inicial",
            "documentación inicial",
            "documentación",
            "documentacion",
            "documentos",
            "papeles",
            "requisitos",
            "qué necesito presentar",
            "que necesito presentar",
            "qué tengo que presentar",
            "que tengo que presentar",
            "para empezar",
            "para comenzar",
            "al comenzar",
            "inicio del tramite",
            "inicio del trámite"
        ]

        palabras_quien_puede = [
            "quién puede",
            "quien puede",
            "puedo hacerlo",
            "puedo realizarlo",
            "particular",
            "profesional",
            "matriculado",
            "matrícula",
            "matricula",
            "arquitecto",
            "ingeniero",
            "maestro mayor"
        ]

        palabras_etapas = [
            "etapas",
            "pasos",
            "proceso",
            "procedimiento",
            "cómo funciona",
            "como funciona",
            "cómo se hace",
            "como se hace",
            "carpeta técnica previa",
            "carpeta tecnica previa",
            "carpeta técnica",
            "carpeta tecnica",
            "certificado provisorio",
            "verificación sanitaria",
            "verificacion sanitaria",
            "presentación final",
            "presentacion final",
            "planos aprobados",
            "retiro de planos",
            "retirar los planos",
            "etapa 1",
            "etapa 2",
            "etapa 3",
            "etapa 4",
            "etapa 5",
            "etapa 6"
        ]

        palabras_lugar_contacto = [
            "dónde",
            "donde",
            "dirección",
            "direccion",
            "teléfono",
            "telefono",
            "horario",
            "contacto",
            "9 de julio",
            "436200"
        ]

        palabras_observaciones = [
            "importante",
            "observación",
            "observacion",
            "observaciones",
            "tener en cuenta",
            "aclaración",
            "aclaracion"
        ]

        es_documentacion_final = any(
            palabra in consulta
            for palabra in palabras_documentacion_final
        )

        if es_documentacion_final:

            secciones_detectadas.append(
                {"nombre": "Documentación final"}
            )

        elif any(
            palabra in consulta
            for palabra in palabras_documentacion_inicial
        ):

            secciones_detectadas.append(
                {"nombre": "Documentación inicial"}
            )

        if any(
            palabra in consulta
            for palabra in palabras_quien_puede
        ):

            secciones_detectadas.append(
                {"nombre": "¿Quién puede realizarlo?"}
            )

        # Solo mostramos etapas si no hay señales de finalización.

        if (
            not es_documentacion_final
            and any(
                palabra in consulta
                for palabra in palabras_etapas
            )
        ):

            secciones_detectadas.append(
                {"nombre": "Etapas del trámite"}
            )

        if any(
            palabra in consulta
            for palabra in palabras_lugar_contacto
        ):

            secciones_detectadas.append(
                {"nombre": "Lugar y contacto"}
            )

        if any(
            palabra in consulta
            for palabra in palabras_observaciones
        ):

            secciones_detectadas.append(
                {"nombre": "Observaciones importantes"}
            )

    return secciones_detectadas


# ============================================================
# BUSCAR SECCIÓN POR SIMILITUD
# ============================================================

def buscar_por_similitud(
    consulta,
    tramite,
    cantidad_resultados=1
):

    documentos = []

    for documento in documentos_secciones:

        if documento["tramite"] == tramite["nombre"]:

            documentos.append(documento)

    if not documentos:
        return []

    textos = [
        documento["texto"]
        for documento in documentos
    ]

    vectorizador = TfidfVectorizer()

    matriz = vectorizador.fit_transform(
        textos + [consulta]
    )

    vector_consulta = matriz[-1]
    vectores_documentos = matriz[:-1]

    similitudes = cosine_similarity(
        vector_consulta,
        vectores_documentos
    ).flatten()

    indices_ordenados = similitudes.argsort()[::-1]

    resultados = []

    for indice in indices_ordenados[
        :cantidad_resultados
    ]:

        resultados.append(
            {
                "nombre": documentos[indice]["seccion"],
                "similitud": similitudes[indice]
            }
        )

    return resultados


# ============================================================
# OBTENER TRÁMITE POR NOMBRE
# ============================================================

def obtener_tramite_por_nombre(
    tramites,
    nombre_tramite
):

    for tramite in tramites:

        if tramite["nombre"] == nombre_tramite:
            return tramite

    return None


# ============================================================
# OBTENER SECCIÓN
# ============================================================

def obtener_seccion(tramite, nombre_seccion):

    for seccion in tramite["secciones"]:

        if seccion["titulo"] == nombre_seccion:
            return seccion

    return None


# ============================================================
# MOSTRAR BLOQUES
# ============================================================

def mostrar_bloques(bloques):

    for bloque in bloques:

        tipo = bloque["tipo"]

        if tipo == "texto":

            st.write(
                bloque["contenido"]
            )

        elif tipo == "lista":

            for elemento in bloque["elementos"]:

                st.write(
                    f"• {elemento}"
                )

        elif tipo == "pasos":

            for numero, elemento in enumerate(
                bloque["elementos"],
                start=1
            ):

                st.write(
                    f"{numero}. {elemento}"
                )

        elif tipo == "advertencia":

            st.warning(
                bloque["contenido"]
            )

        elif tipo == "informacion":

            st.info(
                bloque["contenido"]
            )

        elif tipo == "subseccion":

            with st.expander(
                bloque["titulo"],
                expanded=False
            ):

                mostrar_bloques(
                    bloque["bloques"]
                )


# ============================================================
# CONFIGURACIÓN DE UMBRALES
# ============================================================

UMBRAL_SIMILITUD_SECCION = 0.10

UMBRAL_SIMILITUD_TRAMITE = 0.25


# ============================================================
# INTERFAZ PRINCIPAL
# ============================================================

# Encabezado principal
st.markdown(
    """
    <div class="hero">
        <div class="hero-icon">🏛️</div>
        <div class="hero-title">Trámite Fácil</div>
        <div class="hero-subtitle">
            Información clara y sencilla sobre trámites municipales de Río Grande.
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

# ------------------------------------------------------------
# ACCESIBILIDAD
# Los controles quedan debajo del título y ocupan poco espacio.
# ------------------------------------------------------------

def cambiar_tamano_texto():
    st.session_state.tamano_texto = st.session_state.selector_tamano

col_control_tema, col_control_tamano = st.columns([1, 1])

with col_control_tema:
    if st.button(
        "☀️ Modo claro" if st.session_state.modo_oscuro else "🌙 Modo oscuro",
        help="Cambiar entre modo claro y oscuro",
        key="boton_tema",
        use_container_width=True
    ):
        st.session_state.modo_oscuro = not st.session_state.modo_oscuro
        st.rerun()

with col_control_tamano:
    st.radio(
        "Tamaño del texto",
        ["Normal", "Grande", "Muy grande"],
        index=["Normal", "Grande", "Muy grande"].index(
            st.session_state.tamano_texto
        ),
        key="selector_tamano",
        on_change=cambiar_tamano_texto,
        horizontal=True,
        label_visibility="visible",
    )


# ============================================================
# BUSCADOR
# ============================================================

st.markdown(
    f"""
    <div class="search-card">
        <div class="search-eyebrow">PASO 1 · BUSCÁ LO QUE NECESITÁS</div>
        <h2>🔎 ¿Qué necesitás consultar?</h2>
        <div class="search-description">
            Escribí tu pregunta con tus propias palabras. Por ejemplo:
            <strong>¿Qué documentos necesito para sacar la licencia?</strong>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

def nueva_consulta():
    # Una nueva búsqueda debe tener prioridad sobre la información
    # abierta desde una tarjeta.
    st.session_state.tramite_desde_tarjeta = None

def abrir_tramite(nombre):
    # Callback ejecutado antes de volver a renderizar los widgets.
    # Así evitamos modificar la clave de un widget después de instanciarlo.
    st.session_state.tramite_desde_tarjeta = nombre
    st.session_state.consulta_input = ""

consulta = st.text_input(
    "Escribí tu consulta",
    placeholder=(
        "Ejemplo: tengo 17 años y quiero sacar mi licencia por primera vez"
    ),
    key="consulta_input",
    on_change=nueva_consulta,
)


# Trámite seleccionado desde una tarjeta.
# Se utiliza session_state para que la selección se mantenga después del rerun.
if "tramite_desde_tarjeta" not in st.session_state:
    st.session_state.tramite_desde_tarjeta = None


# ============================================================
# PROCESAR BÚSQUEDA
# ============================================================

if consulta:
    # --------------------------------------------------------
    # PASO 1: DETECTAR TRÁMITE CON REGLAS
    # --------------------------------------------------------
    resultado = detectar_tramite(
        consulta,
        datos["tramites"]
    )

    metodo_deteccion_tramite = "reglas"

    # --------------------------------------------------------
    # PASO 2: TF-IDF COMO RESPALDO
    # --------------------------------------------------------
    if resultado is None:
        resultados_tramite_similitud = buscar_tramite_por_similitud(
            consulta,
            cantidad_resultados=1
        )

        if resultados_tramite_similitud:
            mejor_tramite = resultados_tramite_similitud[0]

            if mejor_tramite["similitud"] >= UMBRAL_SIMILITUD_TRAMITE:
                resultado = obtener_tramite_por_nombre(
                    datos["tramites"],
                    mejor_tramite["nombre"]
                )
                metodo_deteccion_tramite = "similitud"

    # --------------------------------------------------------
    # PASO 3: PEDIR ACLARACIÓN SI NO SE IDENTIFICA EL TRÁMITE
    # --------------------------------------------------------
    if resultado is None:
        st.warning(
            "Necesito un poco más de información para identificar el trámite."
        )

        tramite_aclarado = st.selectbox(
            "¿Sobre cuál trámite querés consultar?",
            [
                "Seleccioná un trámite",
                "Estacionamiento Medido",
                "Licencia de Conducir",
                "Aprobación de Planos"
            ],
            key="tramite_aclaracion"
        )

        if tramite_aclarado != "Seleccioná un trámite":
            st.session_state.tramite_desde_tarjeta = tramite_aclarado
            resultado = obtener_tramite_por_nombre(
                datos["tramites"],
                tramite_aclarado
            )
            metodo_deteccion_tramite = "seleccion_usuario"

    # --------------------------------------------------------
    # CONTINUAR SI HAY UN TRÁMITE
    # --------------------------------------------------------
    if resultado:
        if metodo_deteccion_tramite == "reglas":
            st.success(
                "Entendí que tu consulta está "
                f"relacionada con: **{resultado['nombre']}**"
            )
        elif metodo_deteccion_tramite == "similitud":
            st.info(
                "No encontré una coincidencia exacta, pero encontré un trámite "
                f"relacionado con tu consulta: **{resultado['nombre']}**"
            )
        elif metodo_deteccion_tramite == "seleccion_usuario":
            st.success(
                "Perfecto. Voy a buscar información sobre: "
                f"**{resultado['nombre']}**"
            )

        # ----------------------------------------------------
        # DETECTAR SECCIONES CON REGLAS
        # ----------------------------------------------------
        secciones_detectadas = detectar_secciones(
            consulta,
            resultado
        )

        coincidencia_aproximada = False

        # ----------------------------------------------------
        # TF-IDF COMO RESPALDO PARA SECCIONES
        # ----------------------------------------------------
        if not secciones_detectadas:
            resultados_similitud = buscar_por_similitud(
                consulta,
                resultado,
                cantidad_resultados=1
            )

            if resultados_similitud:
                mejor_resultado = resultados_similitud[0]

                if mejor_resultado["similitud"] >= UMBRAL_SIMILITUD_SECCION:
                    secciones_detectadas.append(
                        {"nombre": mejor_resultado["nombre"]}
                    )
                    coincidencia_aproximada = True

        # ----------------------------------------------------
        # ELIMINAR DUPLICADOS
        # ----------------------------------------------------
        nombres_secciones = []

        for item in secciones_detectadas:
            nombre = item["nombre"]
            if nombre not in nombres_secciones:
                nombres_secciones.append(nombre)

        # ----------------------------------------------------
        # MOSTRAR RESULTADOS DE LA BÚSQUEDA
        # ----------------------------------------------------
        if nombres_secciones:
            if coincidencia_aproximada:
                st.info(
                    "No encontré una coincidencia exacta, pero encontré "
                    "información relacionada con tu consulta."
                )

            st.subheader("📌 Información que puede ayudarte")

            for nombre_seccion in nombres_secciones:
                seccion = obtener_seccion(
                    resultado,
                    nombre_seccion
                )

                if seccion:
                    icono = seccion.get("icono", "📌")

                    with st.expander(
                        f"{icono} {nombre_seccion}",
                        expanded=False
                    ):
                        mostrar_bloques(seccion["bloques"])
                else:
                    st.info(
                        f"La intención detectada fue **{nombre_seccion}**, "
                        "pero todavía no existe una sección con ese nombre "
                        "en los datos del trámite."
                    )
        else:
            st.info(
                "Identifiqué el trámite, pero todavía no pude determinar "
                "qué información específica necesitás."
            )

        # En una búsqueda, la fuente corresponde al resultado mostrado.
        # Se mantiene dentro del bloque de resultados y no se muestra la
        # ficha completa del trámite debajo de las tarjetas.
        st.markdown("### 🔗 Fuente oficial")
        st.markdown(
            f"[{resultado['fuente']['nombre']}]({resultado['fuente']['url']})"
        )


# ============================================================
# ACCESO RÁPIDO A TRÁMITES
# ============================================================

st.markdown(
    f"""
    <div class="quick-access-title">
        O elegí directamente un trámite
    </div>

    <div class="quick-access-description">
        Si preferís no escribir una consulta, elegí uno de los trámites disponibles.
    </div>
    """,
    unsafe_allow_html=True
)


col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(
        """
        <div class="tramite-card">
            <div class="tramite-card-icon">🅿️</div>
            <div class="tramite-card-title">Estacionamiento Medido</div>
            <div class="tramite-card-description">
                Pagos, tarifas, puntos de venta, excepciones e infracciones.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.button(
        "Ver información",
        key="rapido_estacionamiento",
        use_container_width=True,
        on_click=abrir_tramite,
        args=("Estacionamiento Medido",)
    )

with col2:
    st.markdown(
        """
        <div class="tramite-card">
            <div class="tramite-card-icon">🚗</div>
            <div class="tramite-card-title">Licencia de Conducir</div>
            <div class="tramite-card-description">
                Primera licencia, renovación, menores, profesionales y lugares.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.button(
        "Ver información",
        key="rapido_licencia",
        use_container_width=True,
        on_click=abrir_tramite,
        args=("Licencia de Conducir",)
    )

with col3:
    st.markdown(
        """
        <div class="tramite-card">
            <div class="tramite-card-icon">📐</div>
            <div class="tramite-card-title">Aprobación de Planos</div>
            <div class="tramite-card-description">
                Documentación, etapas, responsables, contacto y observaciones.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.button(
        "Ver información",
        key="rapido_planos",
        use_container_width=True,
        on_click=abrir_tramite,
        args=("Aprobación de Planos",)
    )


# ============================================================
# MOSTRAR INFORMACIÓN COMPLETA SOLO SI EL USUARIO LA SOLICITÓ
# ============================================================

tramite_seleccionado = st.session_state.tramite_desde_tarjeta

if tramite_seleccionado and not consulta:
    tramite = obtener_tramite_por_nombre(
        datos["tramites"],
        tramite_seleccionado
    )

    if tramite:
        st.markdown(
            """
            <div class="tramite-header">
                <div class="tramite-header-icon">📋</div>
                <div class="tramite-header-content">
                    <div class="tramite-header-title">
                        Información del trámite
                    </div>
                    <div class="tramite-header-description">
                        Información oficial explicada de forma sencilla.
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

        st.header(f"📄 {tramite['nombre']}")
        st.write(tramite["descripcion"])

        for seccion in tramite["secciones"]:
            icono = seccion.get("icono", "📌")

            with st.expander(
                f"{icono} {seccion['titulo']}",
                expanded=False
            ):
                mostrar_bloques(seccion["bloques"])

        if "informacion_no_disponible" in tramite:
            with st.expander(
                "ℹ️ Información no disponible en la fuente consultada",
                expanded=False
            ):
                for informacion in tramite["informacion_no_disponible"]:
                    st.write(f"• {informacion}")

        # La fuente oficial queda al final, después de toda la información.
        st.markdown(
            "### 🔗 Fuente oficial"
        )
        st.markdown(
            f"[{tramite['fuente']['nombre']}]({tramite['fuente']['url']})"
        )


# ============================================================
# PIE DE PÁGINA
# ============================================================

st.divider()

st.caption(
    "Trámite Fácil organiza y explica información publicada por fuentes oficiales. "
    "Ante cambios o dudas, consultá siempre la fuente oficial correspondiente."
)

