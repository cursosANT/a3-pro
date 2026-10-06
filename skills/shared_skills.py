# Skills compartidas entre varios agentes.
from tools.shared_tools import register_contact, escalate_ticket

SHARED_SKILLS = {
    "register_contact": {
        "description": (
            "Registrar datos de contacto del usuario (email, nombre, motivo). "
            "Úsala cuando el usuario proporcione su correo electrónico para seguimiento."
        ),
        "function": register_contact
    },
    "escalate_ticket": {
        "description": (
            "Escalar un caso para ser atendido por un supervisor humano. "
            "Úsala SOLO cuando el usuario confirme que ya probó las soluciones y el problema persiste. "
            "Debes usar register_contact ANTES de escalar."
        ),
        "function": escalate_ticket
    }
}

SHARED_TOOLS = [skill["function"] for skill in SHARED_SKILLS.values()]