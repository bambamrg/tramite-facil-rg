#  Trámite Fácil

##  Demo

👉 [Probar Trámite Fácil](https://tramite-facil-rg.streamlit.app/)

### Asistente inteligente para facilitar la comprensión de trámites municipales

Trámite Fácil es una aplicación web desarrollada con Python y Streamlit que busca facilitar el acceso a información sobre trámites municipales de la ciudad de Río Grande, Tierra del Fuego.

La aplicación permite realizar consultas utilizando lenguaje natural y obtener información específica sobre diferentes trámites sin necesidad de recorrer manualmente páginas extensas.

También ofrece accesos rápidos, selección manual del trámite y opciones de accesibilidad como modo oscuro y diferentes tamaños de texto.

---

##  Problema

La información sobre trámites públicos puede encontrarse distribuida en diferentes páginas y documentos, lo que puede dificultar que una persona identifique rápidamente:

- qué documentación necesita;
- dónde debe realizar el trámite;
- cuáles son sus etapas;
- quién puede realizarlo;
- cuánto cuesta;
- cuáles son los requisitos;
- qué excepciones existen;
- qué ocurre ante determinadas situaciones.

Trámite Fácil busca reducir esa dificultad mediante una interfaz sencilla que permite realizar preguntas en lenguaje natural.

---

##  Solución

La aplicación organiza la información oficial de los trámites en una estructura de datos propia y utiliza diferentes mecanismos para interpretar las consultas del usuario.

El sistema combina:

- reglas y palabras clave;
- detección del trámite;
- detección de la intención o sección consultada;
- coincidencias aproximadas;
- TF-IDF y similitud coseno como mecanismo de respaldo.

De esta manera, una consulta como:

> "¿Qué documentos necesito para sacar la licencia por primera vez?"

puede ser interpretada como:

```text
Trámite:
Licencia de Conducir

Sección:
Licencia por primera vez