from google import genai
from google.genai import types

MODEL_NAME = "gemini-3.5-flash-lite"

class BaseAgent:
    """
    Clase base que todos los agentes deben heredar.
    - Mantiene un chat persistente (self._chat) para recordar el contexto entre mensajes.
    """
    def __init__(self):
        self.client = genai.Client()
        self.model_name = MODEL_NAME
        # Configuración del agente, redefinido por cada agente específico.
        self.system_instruction = ""
        self.tools = [] 
        self._chat = None

    def _get_chat(self):
        """
        Crea o reutiliza el chat persistente con la configuración actual.
        - Si no existe, lo crea con el system_instruction y tools actuales.
        """
        if self._chat is None:
            config = types.GenerateContentConfig(
                system_instruction=self.system_instruction,
                thinking_config=self._get_thinking_config(),
                tools=self.tools
            )
            self._chat = self.client.aio.chats.create(
                model=self.model_name,
                config=config
            )
        return self._chat
    
    async def generate_response(self, user_message: str) -> str:
        """
        Genera una respuesta usando el chat persistente.
        """
        try:
            chat = self._get_chat()
            response = await chat.send_message(user_message)
            return response.text if response.text else ""
        except Exception as e:
            print(f"Error en {self.__class__.__name__}: {e}")
            return ""  # Fallback: respuesta vacía, el orquestador elegirá otra.

    def _get_thinking_config(self) -> float:
        """Razonamiento para este agente. Puede ser sobreescrito por cada agente hijo."""
        return types.ThinkingConfig(thinking_level=types.ThinkingLevel.MEDIUM)