# Este es el "cerebro" del sistema multiagente. Clasifica y delega consultas a agentes especializados.
import asyncio
from google import genai
from google.genai import types
from agents.sales_agent import SalesAgent
from agents.support_agent import SupportAgent
from agents.billing_agent import BillingAgent
from utils.json_utils import save_conversation

MODEL_NAME = "gemini-3.5-flash-lite"

class Orchestrator:
    """
    El "cerebro" del sistema multiagente. Responsabilidades:
    1. Clasificar la intención del usuario (VENTAS, SOPORTE, FACTURACIÓN).
    2. Delegar la consulta a los agentes especializados.
    4. Seleccionar la mejor respuesta mediante un sistema de puntuación.
    """
    def __init__(self):
        # Agentes especializados
        self.sales_agent = SalesAgent()
        self.support_agent = SupportAgent()
        self.billing_agent = BillingAgent()

        self.client = genai.Client()
        
        # Prompt del sistema
        self.classifier_instruction = """
Eres A3, un clasificador de intenciones para Cursos ANT.
Clasifica la consulta del usuario en una de estas categorías:
VENTAS, SOPORTE, FACTURACIÓN o DESCONOCIDO.

Responde solo con la palabra de la categoría.
"""

        # Mapeo de clasificaciones a agentes
        self.agent_mapping = {
            "VENTAS": [self.sales_agent],
            "SOPORTE": [self.support_agent],
            "FACTURACIÓN": [self.billing_agent]
        }

    async def handle_query(self, user_message: str, history: list) -> str:
        """
        Flujo: clasifica, ejecuta agentes en paralelo, selecciona la mejor respuesta.
        - 'history': lista con el contexto de la conversación.
        """
        # 1. Clasificar la intención usando un modelo de IA
        classification = await self._classify(user_message, history)
        print(f"📌 Clasificación: {classification}")

        # 2. Seleccionar agentes según clasificación
        agents = self._get_agents_for_classification(classification)

        # 3. Ejecutar agentes en paralelo
        responses = await self._run_agents_in_parallel(agents, user_message, history)

        # 4. Seleccionar la mejor respuesta
        best_response = self._select_best_response(responses)

        # 5. Guardar conversación en JSON para auditoría o análisis posterior
        save_conversation(user_message, best_response)

        return best_response

    def _get_agents_for_classification(self, classification: str) -> list:
        """
        Retorna el(los) agentes a ejecutar según la clasificación.
        Si no se reconoce la categoría (DESCONOCIDO), devuelve TODOS los agentes como fallback.
        Esto asegura que el usuario siempre reciba una respuesta.
        """
        if classification in self.agent_mapping:
            return self.agent_mapping[classification]

        # Fallback: devolver todos los agentes
        print("🔄 Clasificación desconocida, ejecutando todos los agentes...")
        return [self.sales_agent, self.support_agent, self.billing_agent]

    async def _run_agents_in_parallel(self, agents: list, user_message: str, history: list) -> list:
        """
        Ejecuta múltiples agentes en paralelo usando asyncio.gather.
        Retorna una lista de respuestas o excepciones.
        """
        tasks = [agent.generate_response(user_message) for agent in agents]
        return await asyncio.gather(*tasks, return_exceptions=True)

    def _score_response(self, text: str) -> int:
        """
        Sistema de puntuación para evaluar la calidad de cada respuesta.
        Basado en longitud, presencia de información concreta, etc.
        """
        if not text:
            return 0

        score = 0

        # Criterio 1: Longitud
        if len(text) > 200:
            score += 3
        elif len(text) > 150:
            score += 2
        elif len(text) > 100:
            score += 1

        # Criterio 2: Información concreta
        concrete = ["$", "claro", "paso", "1.", "2.", "- ", "precio", "curso", "clase"]
        if any(word in text.lower() for word in concrete):
            score += 2

        # Criterio 3: Penalización por falta de confianza
        uncertainty = ["no sé", "no puedo", "disculpa", "lo siento", "no encontré"]
        if any(word in text.lower() for word in uncertainty):
            score -= 2

        # Criterio 4: Bonus por fomenta interacción.
        if text.strip().endswith("?"):
            score += 1

        # Criterio 5: Bonus por contener números
        if any(char.isdigit() for char in text):
            score += 1

        return score

    def _select_best_response(self, results: list) -> str:
        """Selecciona la mejor respuesta usando el sistema de puntuación."""
        best_response = ""
        best_score = float('-inf')

        for response in results:
            if isinstance(response, Exception):
                print(f"⚠️ Error en agente: {response}")
                continue
            if not response:
                continue

            current_score = self._score_response(response)
            print(f"📊 Puntuación: {current_score} - {response[:30]}...")

            # Elegir la respuesta con mayor puntuación
            if current_score > best_score:
                best_score = current_score
                best_response = response

        # Fallback: si no hay respuesta válida, mensaje genérico
        return best_response or "Lo siento, no pude procesar tu consulta. ¿Podrías reformularla?"

    async def _classify(self, user_message: str, history: list) -> str:
        """Clasifica la intención del usuario usando Gemini.
        - Utiliza el historial reciente (últimos 3 mensajes) como contexto.
        - El resultado es una categoría (VENTAS, SOPORTE, FACTURACIÓN) o DESCONOCIDO.
        """
        context = ""
        for msg in history[-3:]:
            role = "Usuario" if msg["role"] == "user" else "Asistente"
            context += f"{role}: {msg['content']}\n"
        
        prompt = f"""
Basado en el historial reciente, clasifica la última consulta:

------ Historial ------
{context}
-----------------------

Última consulta: "{user_message}"

Categoría (VENTAS, SOPORTE, FACTURACIÓN)
"""
        thinking_config = types.ThinkingConfig(thinking_level=types.ThinkingLevel.MINIMAL)
        config = types.GenerateContentConfig(
            system_instruction=self.classifier_instruction,
            thinking_config=thinking_config
        )
        try:
            chat = self.client.aio.chats.create(
                model=MODEL_NAME, 
                config=config
            )
            response = await chat.send_message(prompt)
            classification = response.text.strip().upper()

            # Validar que sea una categoría conocida
            if classification in self.agent_mapping:
                return classification

            print(f"⚠️ Clasificación no reconocida: '{classification}'")
            return "DESCONOCIDO"  # Fallback: no se pudo clasificar

        except Exception as e:
            print(f"❌ Error en clasificador: {e}")
            return "DESCONOCIDO"  # Fallback por error