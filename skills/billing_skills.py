from tools.sales_tools import get_product_info

BILLING_SKILLS = {
    "get_product_info": {
        "description": (
            "Obtener el precio de un curso del catálogo. "
            "Úsala SIEMPRE que el cliente pregunte por precios."
        ),
        "function": get_product_info
    }
}

BILLING_TOOLS = [skill["function"] for skill in BILLING_SKILLS.values()]