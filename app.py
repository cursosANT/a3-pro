import os
import gradio as gr
from dotenv import load_dotenv
from orchestrator import Orchestrator

load_dotenv(override=True)

orchestrator = Orchestrator()

async def chat(message: str, history: list) -> str:
    """Maneja cada mensaje. Retorna respuesta del agente o mensaje de error."""
    try:
        response = await orchestrator.handle_query(message, history)
        return response if response else "Lo siento, no pude procesar tu consulta. ¿Podrías intentar de nuevo?"
    except Exception as e:
        print(f"Error en chat: {e}")
        return "Ocurrió un error. Por favor, intenta de nuevo."

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 7860))

    gr.ChatInterface(
        fn=chat, 
        title="A3 Pro", 
        description="Hola, ¿Cómo podemos ayudarte?").launch(
            server_name="0.0.0.0",
            server_port=port
        )