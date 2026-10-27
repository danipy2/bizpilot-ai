"""
BizPilot AI — Inventory Tool
Agent tool for searching and checking inventory from the database.
"""

from langchain.tools import tool
from database.db import search_inventory, get_low_stock_products, get_product_by_sku


@tool
def check_inventory(query: str = "", category: str = "") -> str:
    """
    Search the business inventory for products.
    Use this tool when the user asks about products, stock levels, prices, or inventory.

    Args:
        query: Product name or SKU to search for. Leave empty to list all.
        category: Filter by category (Electronics, Furniture, Supplies, Accessories, Beverages).

    Returns:
        Formatted inventory results with name, SKU, price, stock, and category.
    """
    products = search_inventory(query, category)

    if not products:
        return f"No products found matching '{query}' in category '{category}'."

    results = []
    for p in products:
        stock_status = "⚠️ LOW STOCK" if p["stock_quantity"] <= 10 else "✅ In Stock"
        results.append(
            f"• {p['name']} (SKU: {p['sku']})\n"
            f"  Price: {p['price']:,.2f} ETB | Stock: {p['stock_quantity']} units | {stock_status}\n"
            f"  Category: {p['category']} | {p['description']}"
        )

    return f"Found {len(products)} products:\n\n" + "\n\n".join(results)


@tool
def get_low_stock_alerts(threshold: int = 15) -> str:
    """
    Get products with low stock levels that need reordering.
    Use this tool when the user asks about low stock, reordering, or stock alerts.

    Args:
        threshold: Stock level threshold (default 15). Products at or below this level are flagged.

    Returns:
        List of low-stock products with quantities and reorder suggestions.
    """
    products = get_low_stock_products(threshold)

    if not products:
        return f"All products have stock levels above {threshold} units. No reordering needed."

    results = ["🚨 LOW STOCK ALERT — Products needing reorder:\n"]
    for p in products:
        urgency = "🔴 CRITICAL" if p["stock_quantity"] <= 5 else "🟡 WARNING"
        results.append(
            f"{urgency} {p['name']} (SKU: {p['sku']})\n"
            f"   Current Stock: {p['stock_quantity']} units | Price: {p['price']:,.2f} ETB"
        )

    return "\n\n".join(results)
