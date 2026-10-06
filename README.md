# A3 Pro - Sistema Multiagente para Atención al Cliente

A3 Pro es un sistema de agentes de IA especializados que simulan un equipo de atención al cliente para una empresa de cursos online (Cursos ANT). Está construido con Python y Gemini, y utiliza un orquestador para clasificar consultas y delegar a agentes especializados en ventas, soporte y facturación.

## ✨ Características

- **Multiagente:** Agentes especializados (SalesAgent, SupportAgent, BillingAgent) con responsabilidades únicas.
- **Orquestador:** Clasifica la intención del usuario y delega al agente adecuado.
- **Ejecución en paralelo:** Uso de `asyncio.gather` para consultar varios agentes simultáneamente.
- **Selección de mejor respuesta:** Sistema de puntuación heurística para elegir la respuesta más completa.
- **Fallback:** Si la clasificación falla, se ejecutan todos los agentes y se elige la mejor respuesta.
- **Skills y Tools:** Organización modular de capacidades y funciones Python.
- **Chat persistente:** Cada agente mantiene el contexto de la conversación.
- **Datos externos:** Catálogo, FAQs e incidencias en archivos JSON/TXT para fácil actualización.
- **Interfaz web:** Chat interactivo con Gradio.
- **Auditoría:** Guardado de conversaciones en `conversations.json`.


## 🛠️ Requisitos

- Python 3.12 o superior
- [UV](https://github.com/astral-sh/uv) como gestor de paquetes (recomendado)
- Cuenta en Google AI Studio para obtener una API Key de Gemini

## 🚀 Instalación

1. Clona el repositorio o descarga los archivos.

2. Crea y activa un entorno virtual con UV:
    ```bash
    uv init
    uv venv
    source .venv/bin/activate  # macOS/Linux
    .venv\Scripts\activate     # Windows

3. Instala las dependencias:
    ```bash
    uv add google-genai gradio python-dotenv requests

- **O si usas requirements.txt:**
    uv pip install -r requirements.txt

4. Configura las variables de entorno:
- Crea .env.
- Edita .env y añade tu API Key: GOOGLE_API_KEY=tu_api_key_aqui

## ▶️ Uso
Ejecuta la aplicación:
    ```bash
    python app.py

Se abrirá una interfaz web (Gradio) en tu navegador. Escribe tus consultas y el sistema clasificará y delegará automáticamente al agente adecuado.

## 🧠 ¿Cómo funciona?
- El usuario envía un mensaje.
- El Orquestador clasifica la intención: VENTAS, SOPORTE o FACTURACIÓN.
- Se ejecutan los agentes correspondientes en paralelo.
- Cada agente usa sus skills (herramientas) para generar una respuesta.
- El Orquestador puntúa las respuestas y elige la mejor.
- La conversación se guarda en conversations.json para auditoría.

## 📚 Datos personalizables
- Puedes modificar los archivos en data/ para adaptar el sistema a tu propio negocio:
- cursos_ant.txt: información general de la empresa.
- catalog.json: productos/servicios con precios y características.
- faq.json: preguntas frecuentes y respuestas.
- issues.json: errores conocidos y soluciones.

## 📝 Licencia
Este proyecto es parte de un curso educativo. Como estudiante Premium, puedes usarlo y modificarlo libremente.