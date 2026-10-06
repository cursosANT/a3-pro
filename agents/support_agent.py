from agents.base_agent import BaseAgent
from skills.support_skills import SUPPORT_SKILLS, SUPPORT_TOOLS
from skills.shared_skills import SHARED_SKILLS, SHARED_TOOLS
from pathlib import Path
from google.genai import types

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
COMPANY_FILE = DATA_DIR / "cursos_ant.txt"

class SupportAgent(BaseAgent):
    """Agente de soporte. Resuelve problemas técnicos paso a paso."""
    def __init__(self):
        super().__init__()
        # Combinar skills de soporte + skills compartidas (registro de contacto y escalado)
        self.tools = SUPPORT_TOOLS + SHARED_TOOLS

        # Carga de información de la empresa (permite responder preguntas generales)
        self.info = ""
        if COMPANY_FILE.exists():
            with open(COMPANY_FILE, "r", encoding="utf-8") as file:
                self.info = file.read()

        skills_desc = "\n".join([
            f"- {name}: {info['description']}"
            for name, info in SUPPORT_SKILLS.items()
        ])

        shared_skills_desc = "\n".join([
            f"- {name}: {info['description']}"
            for name, info in SHARED_SKILLS.items()
        ])
        
        self.system_instruction = f"""
Eres A3 Soporte, el agente de soporte técnico de Cursos ANT.

### Tu trabajo:
- Escucha el problema del usuario y pide detalles si faltan.
- Usa las skills disponibles para encontrar soluciones.
- Si no encuentras una solución, informa al usuario y forece contacto humano.

### Skills disponibles:
{skills_desc}

### Skills compartidas (para escalar o registrar):
{shared_skills_desc}

### Comportamiento con el cliente:
- Sé claro, paciente y profesional.
- No inventes soluciones. Todo debe venir de las skills.

### Importante:
- Antes de escalar: Pide el email del usuario, el nombre, luego registralo y procede a escalar.

Información de la empresa o instructor:
{self.info}
"""

    def _get_thinking_config(self) -> float:
            """Razonamiento para este agente. Respuestas más precisas y consistentes."""
            return types.ThinkingConfig(thinking_level=types.ThinkingLevel.LOW)