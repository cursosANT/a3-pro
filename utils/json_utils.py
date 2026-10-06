import json
from pathlib import Path
from datetime import datetime

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
HISTORY_FILE = DATA_DIR / "history.json"

def save_conversation(user_msg: str, agent_response: str) -> None:
    """
    Guarda la conversación en un archivo JSON para auditoría o análisis posterior.
    - Útil para depuración y para construir datasets de entrenamiento.
    """
    data = []
    if HISTORY_FILE.exists():
        with open(HISTORY_FILE, "r", encoding="utf-8") as file:
            try:
                data = json.load(file)
            except json.JSONDecodeError:
                data = []

    data.append({
        "timestamp": datetime.now().isoformat(),
        "user": user_msg,
        "agent": agent_response
    })

    with open(HISTORY_FILE, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)