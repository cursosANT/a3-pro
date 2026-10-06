import json
import os
import certifi
from sendgrid import SendGridAPIClient
from sendgrid import Mail
from pathlib import Path
from typing import Any

os.environ["SSL_CERT_FILE"] = certifi.where()

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
FAQ_FILE = DATA_DIR / "faq.json"        # Base de conocimiento para preguntas frecuentes
ISSUES_FILE = DATA_DIR / "issues.json"  # Base de conocimiento para errores técnicos

# Datos por defecto (fallback: si no existen los archivos JSON)
DEFAULT_FAQ = {
    "login": [
        "Problemas de acceso: Usa 'olvidé mi contraseña' en login.cursosant.com",
        "Si no recibes el correo, revisa spam o espera 5 minutos"
    ]
}

DEFAULT_ISSUES = {
    "404": "Página no encontrada: Verifica que la URL sea correcta."
}

def _load_json(file_path, default_data):
    """Carga un archivo JSON o devuelve los datos por defecto (fallback)."""
    if file_path.exists():
        with open(file_path, "r", encoding="utf-8") as file:
            return json.load(file)
    return default_data

faq_data = _load_json(FAQ_FILE, DEFAULT_FAQ)
issues_data = _load_json(ISSUES_FILE, DEFAULT_ISSUES)

def search_faq(keyword: str) -> list[str]:
    """
    Busca soluciones en la base de conocimiento (FAQ) basándose en una palabra clave.
    Args:
        keyword: Palabra o término clave a buscar.
    Returns:
        list[str]: Una lista de cadenas de texto con las soluciones encontradas o
                    con instrucciones de contacto si no hay resultados.
    """
    print(f"📂 Buscando FAQ en: {FAQ_FILE}")
    keyword_lower = keyword.lower()
    results = []

    for key, articles in faq_data.items():
        if key in keyword_lower or keyword_lower in key:
            for article in articles:
                results.append(article)

    if not results:
        return [
            "No encontré una solución para tu caso.",
            "Puedes escribirnos a help@cursos.ant para atención personalizada."
        ]
    return results

def diagnose_issue(error_code: str | None = None, description: str | None = None) -> dict[str, Any]:
    """
    Diagnostica problemas técnicos basados en código o descripción.
    Args:
        error_code (str, opcional): El código de error reportado (ej. '401', 'timeout').
        description (str, opcional): Explicación en texto libre del problema.
    Returns:
        dict[str, Any]: Un diccionario con el diagnóstico:
            - Éxito: {'found': True, 'solution': str, 'next_steps': str}
            - Fallback: {'found': False, 'message': str}
    """
    print(f"📂 Buscando ISSUES en: {ISSUES_FILE}")
    if error_code and error_code in issues_data:
        return {
            "found": True,
            "solution": issues_data[error_code],
            "next_steps": "Si el problema persiste, contacta a soporte@cursosant.com"
        }
    if description:
        if any(word in description.lower() for word in ["error", "falla", "problema"]):
            return {
                "found": True,
                "solution": "Parece un problema técnico. Intenta: 1) Recargar 2) Limpiar caché 3) Otro navegador",
                "next_steps": "Si no funciona, contacta a soporte@cursosant.com"
            }
    return {
        "found": False,
        "message": "No pude diagnosticar automáticamente. Contacta a soporte@cursosant.com"
    }

def send_email(to_email: str, subject: str, body: str) -> dict:
    """
    Envía un correo eletrónico al destinatario indicado usando SendGrid.
        Args:
            to_email (str): Dirección del correo del destinatario.
            subject (str): Asunto del correo.
            body (str): Cuerpo del correo(puede incluir HTML).
        Returns:
            dict[str, str]: Un diccionario con el status(success/error):
                - Éxito: {'status': 'success', 'status_code': str}
                - Fallback: {'status': 'error', 'message': str}
    """
    message = Mail(
        from_email="anicolastello.cursos@gmail.com",
        to_emails=to_email,
        subject=subject,
        html_content=body
    )

    try:
        sg = SendGridAPIClient(os.environ.get("SENDGRID_API_KEY"))
        response = sg.send(message=message)
        print(f"✅ Correo enviado(status = {response.status_code})")
        return {"status": "success", "status_code": response.status_code}
    except Exception as e:
        print(f"❌ Error al enviar email: {e}")
        return {"status": "error", "message": str(e)}