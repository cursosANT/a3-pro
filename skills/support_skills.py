from tools.support_tools import search_faq, diagnose_issue, send_email

SUPPORT_SKILLS = {
    "search_faq": {
        "description": (
            "Buscar soluciones en la base de conocimiento (FAQ). "
            "Úsala siempre que el usuario tenga una duda, problema o consulta."
        ),
        "function": search_faq
    },
    "diagnose_issue": {
        "description": (
            "Diagnosticar problemas técnicos basados en código de error o descripción. "
            "Úsala cuando el usuario mencione un error, falla, código de error o problema técnico."
        ),
        "function": diagnose_issue
    },
    "send_email": {
            "description": (
                "Enviar un correo eletrónico de seguimiento al cliente. "
                "Úsala cuando necesites dar seguimiento formal a un caso, enviar "
                "confirmaciones o responder por correo. Requiere el email del destinatario, "
                "un asunto y un cuerpo(puede incluir HTML)."
            ),
            "function": send_email
        }
}

SUPPORT_TOOLS = [skill["function"] for skill in SUPPORT_SKILLS.values()]