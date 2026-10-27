"""
BizPilot AI — Sales Analytics Tool
Agent tool for generating sales summaries and business insights.
"""

from langchain.tools import tool
from database.db import get_sales_summary, get_customer_list


@tool
def summarize_sales(days: int = 7) -> str:
    """
    Generate a comprehensive sales summary report.
    Use this tool when the user asks about sales, revenue, business performance, or daily summary.

    Args:
        days: Number of days to include in the summary (default 7).

    Returns:
        Formatted sales report with revenue, top products, category breakdown, and trends.
    """
    summary = get_sales_summary(days)

    # Format top products
    top_products = "\n".join(
        f"  {i+1}. {p['name']}: {p['revenue']:,.2f} ETB ({p['units_sold']} units)"
        for i, p in enumerate(summary["top_products"])
    )

    # Format category breakdown
    categories = "\n".join(
        f"  • {c['category']}: {c['revenue']:,.2f} ETB"
        for c in summary["revenue_by_category"]
    )

    # Format daily trend
    daily = "\n".join(
        f"  📅 {d['date']}: {d['revenue']:,.2f} ETB ({d['orders']} orders)"
        for d in summary["daily_trend"][-7:]  # Show last 7 days max
    )

    report = f"""
📊 SALES SUMMARY — Last {days} Days
{'━' * 45}

💰 Total Revenue:      {summary['total_revenue']:>15,.2f} ETB
📦 Total Orders:       {summary['total_orders']:>15,}
📊 Avg Order Value:    {summary['average_order_value']:>15,.2f} ETB

🏆 Top Products by Revenue:
{top_products}

📁 Revenue by Category:
{categories}

📈 Daily Trend:
{daily}
{'━' * 45}
"""
    return report


@tool
def list_customers() -> str:
    """
    Get the list of all registered customers with their contact information.
    Use this tool when the user asks about customers, client list, or contact information.

    Returns:
        Formatted list of all customers with name, email, phone, and address.
    """
    customers = get_customer_list()

    if not customers:
        return "No customers found in the database."

    results = [f"👥 CUSTOMER LIST — {len(customers)} customers\n{'━' * 40}\n"]
    for c in customers:
        results.append(
            f"👤 {c['name']}\n"
            f"   📧 {c['email']}\n"
            f"   📞 {c['phone']}\n"
            f"   📍 {c['address']}"
        )

    return "\n\n".join(results)
