from tools.sales_tools import get_product_info, calculate_discount

SALES_SKILLS = {
    "get_product_info": {
        "description": (
            "Consultar información de cursos disponibles (precios, características, nombres). "
            "Úsala SIEMPRE que el cliente pregunte por cursos, precios o características. "
            "Si el cliente pregunta por todos los cursos, invoca esta skill varias veces (una por cada curso)."
        ),
        "function": get_product_info
    },
    "calculate_discount": {
        "description": (
            "Calcular precios finales con descuento. "
            "Úsala cuando el cliente pregunte por descuentos o promociones."
        ),
        "function": calculate_discount
    }
}

SALES_TOOLS = [skill["function"] for skill in SALES_SKILLS.values()]