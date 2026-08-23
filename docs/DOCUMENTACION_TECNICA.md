# Documentación técnica — Trámite Fácil

## 1. Descripción

Trámite Fácil es una aplicación web desarrollada en Python y Streamlit para facilitar la consulta de información sobre trámites municipales.

La aplicación recibe una consulta en lenguaje natural, identifica el trámite relacionado y determina qué sección de información está solicitando el usuario.

---

# 2. Arquitectura general

El sistema está compuesto por cuatro componentes principales:

1. Interfaz de usuario.
2. Datos estructurados.
3. Motor de detección.
4. Mecanismo de respaldo mediante similitud textual.

```text
Usuario
   │
   ▼
Streamlit
   │
   ▼
Consulta en lenguaje natural
   │
   ▼
Normalización
   │
   ├───────────────┐
   ▼               ▼
Detección       Detección
del trámite      de sección
   │               │
   └───────┬───────┘
           ▼
     Recuperación
      información
           │
           ▼
        Respuesta