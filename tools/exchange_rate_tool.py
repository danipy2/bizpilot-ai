"""
BizPilot AI — Exchange Rate Tool
Agent tool for fetching real-time currency exchange rates.
"""

import httpx
from langchain.tools import tool

import config


# Fallback rates if API is unavailable (approximate ETB rates)
FALLBACK_RATES = {
    "USD": 56.50,
    "EUR": 61.30,
    "GBP": 71.20,
    "SAR": 15.07,
    "AED": 15.39,
    "KES": 0.44,
    "CNY": 7.80,
    "INR": 0.68,
    "JPY": 0.38,
    "CAD": 41.50,
}


@tool
def get_exchange_rate(
    from_currency: str = "USD",
    to_currency: str = "ETB",
    amount: float = 1.0,
) -> str:
    """
    Get current exchange rate between two currencies.
    Use this tool when the user asks about currency conversion, exchange rates, or converting money.

    Args:
        from_currency: Source currency code (e.g., USD, EUR, GBP).
        to_currency: Target currency code (e.g., ETB, USD, EUR). Default is ETB.
        amount: Amount to convert (default 1.0).

    Returns:
        Exchange rate information and converted amount.
    """
    from_currency = from_currency.upper().strip()
    to_currency = to_currency.upper().strip()

    # Try live API first
    try:
        api_key = config.EXCHANGE_RATE_API_KEY
        if api_key and api_key != "your_key_here":
            url = f"https://v6.exchangerate-api.com/v6/{api_key}/pair/{from_currency}/{to_currency}/{amount}"
            response = httpx.get(url, timeout=10)
            data = response.json()

            if data.get("result") == "success":
                rate = data["conversion_rate"]
                converted = data["conversion_result"]
                return (
                    f"💱 Exchange Rate: 1 {from_currency} = {rate:,.4f} {to_currency}\n"
                    f"💰 {amount:,.2f} {from_currency} = {converted:,.2f} {to_currency}\n"
                    f"📅 Source: ExchangeRate-API (live)"
                )
    except Exception:
        pass  # Fall through to fallback rates

    # Use fallback rates (ETB-based)
    if to_currency == "ETB" and from_currency in FALLBACK_RATES:
        rate = FALLBACK_RATES[from_currency]
        converted = amount * rate
        return (
            f"💱 Exchange Rate: 1 {from_currency} ≈ {rate:,.2f} {to_currency}\n"
            f"💰 {amount:,.2f} {from_currency} ≈ {converted:,.2f} {to_currency}\n"
            f"📅 Source: Approximate rates (for live rates, configure EXCHANGE_RATE_API_KEY)"
        )
    elif from_currency == "ETB" and to_currency in FALLBACK_RATES:
        rate = 1 / FALLBACK_RATES[to_currency]
        converted = amount * rate
        return (
            f"💱 Exchange Rate: 1 {from_currency} ≈ {rate:,.4f} {to_currency}\n"
            f"💰 {amount:,.2f} {from_currency} ≈ {converted:,.2f} {to_currency}\n"
            f"📅 Source: Approximate rates"
        )
    else:
        return (
            f"Exchange rate for {from_currency} to {to_currency} is not available in fallback data. "
            f"Available currencies: {', '.join(FALLBACK_RATES.keys())} (against ETB). "
            f"Configure EXCHANGE_RATE_API_KEY for full currency support."
        )
