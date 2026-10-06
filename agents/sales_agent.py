from agents.base_agent import BaseAgent
from skills.sales_skills import SALES_SKILLS, SALES_TOOLS
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
COMPANY_FILE = DATA_DIR / "cursos_ant.txt"

class SalesAgent(BaseAgent):
    """Asesor de ventas. Recomienda cursos según las necesidades del cliente."""
    def __init__(self):
        super().__init__()
        # Asignar las tools de ventas.
        self.tools = SALES_TOOLS

        # Carga de información de la empresa (permite responder preguntas generales)
        self.info = ""
        if COMPANY_FILE.exists():
            with open(COMPANY_FILE, "r", encoding="utf-8") as file:
                self.info = file.read()

        # Construir descripción de skills para el prompt (dinámico, se genera desde SALES_SKILLS)
        skills_desc = "\n".join([
            f"- {name}: {info['description']}"
            for name, info in SALES_SKILLS.items()
        ])

        self.system_instruction = f"""
Eres A3 Ventas, asesor de Cursos ANT. Ayudas a clientes a elegir cursos y respondes dudas sobre la empresa.

### Tu trabajo:
- Escucha al cliente y entiende qué quiere.
- Si pregunta por cursos o precios, usa las skills disponibles.
- Si pregunta sobre la empresa o el fundador/instructor, usa la información del final.

### Reglas:
- Responde con ella de forma clara y natural.
- Si no encuentras la respuesta en la información, pide más detalles.
- NUNCA inventes datos que no estén en la información proporcionada.

### Skills disponibles:
{skills_desc}

### Comportamiento:
- Habla en lenguaje natural, sin tecnicismos.
- Traduce lo que el cliente dice a búsquedas en el catálogo o en la información de la empresa.

### INFORMACIÓN DE LA EMPRESA:
{self.info}
"""