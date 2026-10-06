import json
from pathlib import Path
from typing import Any

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
CATALOG_FILE = DATA_DIR / "catalog.json" #

def _load_catalog() -> dict[str, dict[str, Any]] | None: #
    """
    Carga el catálogo de cursos desde el archivo JSON externo.
    Args:
        
    Returns:
        dict | None: Diccionario con el id, nombre, precio y características 
            de cada curso, o None si no existe.
    """
    print(f"📂 Buscando catálogo en: {CATALOG_FILE}")
    if CATALOG_FILE.exists():
        with open(CATALOG_FILE, "r", encoding="utf-8") as file:
            return json.load(file)
    return None 

def get_product_info(product_id: str) -> dict[str, Any]: #              reto type hints mejorado
    """
    Busca y devuelve información de un curso del catálogo.
    Args:
        product_id (str): El identificador único del curso (ej. 'COURSE_01').
    Returns:
        dict: Un diccionario que varía según el resultado:
            - Éxito: {'id', 'name', 'price', 'features', 'full_description'}
            - Error: {'error'} o {'error', 'available_courses'}
    """
    catalog = _load_catalog()
    if catalog is None:
        return {
            "error": "Catálogo no disponible. Contacta a soporte@cursosant.com"
        }

    product = catalog.get(product_id)
    if not product:
        available = "\n".join( # k = key, v = value
            f"- {k}: {v['name']} (${v['price']})" for k, v in catalog.items()
        )
        return {
            "error": f"Producto '{product_id}' no encontrado.",
            "available_courses": available
        }

    features_text = "\n".join(f"  • {f}" for f in product["features"])
    return {
        "id": product_id,
        "name": product["name"],
        "price": f"${product['price']}",
        "features": features_text,
        "full_description": f"""
📚 {product['name']}
💰 Precio: ${product['price']}
✨ Características:
{features_text}
        """
    }

def calculate_discount(price: float, discount_percent: float) -> float:
    """
    Calcula el precio final aplicando un porcentaje de descuento.
    Args:
        price: Precio original del curso.
        discount_percent: Porcentaje de descuento a aplicar.
    Returns:
        float: Resultado de la operación con el precio final.
    """
    return round(price * (1 - discount_percent / 100), 2)