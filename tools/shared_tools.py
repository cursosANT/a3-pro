# Herramientas comunes, compartidas entre varios agentes.
def register_contact(email: str, name: str, reason: str) -> dict[str, str]:
    """
    Registra un contacto para el seguimiento correspondiente.
    Args:
        email: Correo electrónico del usuario.
        name: Nombre del usuario.
        reason: Intención del usuario, motivo de contacto.
    Returns:
        dict: Resultado de la operación con estatus.
    """
    print(f"📌 Contacto registrado: {name} - {email} - Motivo: {reason}")
    return {"status": "success"}

def escalate_ticket(issue: str, urgency: str = "media", email: str = None) -> dict[str, str]:
    """
    Escala un ticket para supervisión humana.
    Args:
        issue: Problema del usuario.
        urgency: Nivel de urgencia.
        email: Correo electrónico del usuario.
    Returns:
        dict: Resultado de la operación con estatus y correo.
    """
    print(f"🛠️ Ticket escalado: {issue} (urgencia: {urgency})")
    if email:
        print(f"📧 Contacto: {email}")
    return {"status": "escalated", "email": email}