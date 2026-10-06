from agents.base_agent import BaseAgent
from skills.billing_skills import BILLING_SKILLS, BILLING_TOOLS
from skills.shared_skills import SHARED_SKILLS, SHARED_TOOLS

class BillingAgent(BaseAgent):
    """Agente de facturación. Consulta precios y orienta sobre pagos."""
    def __init__(self):
        super().__init__()
        # Combinar tools de facturación + compartidas.
        self.tools = BILLING_TOOLS + SHARED_TOOLS

        skills_desc = "\n".join([
            f"- {name}: {info['description']}"
            for name, info in BILLING_SKILLS.items()
        ])

        shared_desc = "\n".join([
            f"- {name}: {info['description']}"
            for name, info in SHARED_SKILLS.items()
        ])

        self.system_instruction = f"""
Eres A3 Facturación, de Cursos ANT. Resuelves dudas sobre pagos, facturas y reembolsos.

### Tu trabajo:
- Escucha al cliente sobre facturación y pagos.
- Usa las skills disponibles para obtener información real.

### Skills disponibles:
{skills_desc}

{shared_desc}

### Comportamiento con el cliente:
- No inventes precios.
- Sé claro y directo con la información financiera.
- Si el caso es complejo (reembolso, factura específica, urgente), pide email y escala.

### Importante:
- Siempre consulta la skill correspondiente antes de responder.
"""