"""
Order Placement Module.

Provides a single entry-point, ``place_order()``, that validates inputs,
dispatches the request to the Binance Futures Testnet API, and returns
a clean response dictionary.
"""

import logging

from binance.exceptions import BinanceAPIException
from requests.exceptions import ConnectionError, Timeout

from bot.client import get_client
from bot.validators import (
    validate_symbol,
    validate_side,
    validate_order_type,
    validate_quantity,
    validate_price,
)

logger = logging.getLogger(__name__)


def place_order(
    symbol: str,
    side: str,
    order_type: str,
    quantity: float,
    price: float | None = None,
) -> dict:
    """
    Validate inputs and place an order on Binance Futures Testnet.

    Args:
        symbol: Trading pair (e.g. ``"BTCUSDT"``).
        side: ``"BUY"`` or ``"SELL"``.
        order_type: ``"MARKET"`` or ``"LIMIT"``.
        quantity: Quantity to trade (positive float).
        price: Limit price (required for LIMIT orders, ignored for MARKET).

    Returns:
        dict: A sanitised response with the following keys:
            ``orderId``, ``symbol``, ``side``, ``type``, ``status``,
            ``executedQty``, ``avgPrice``.

    Raises:
        ValueError: If any input fails validation.
        BinanceAPIException: If the Binance API rejects the order.
        ConnectionError | Timeout: On network-level failures.
    """
    # ── 1. Validate inputs ──────────────────────────────────────────
    symbol = validate_symbol(symbol)
    side = validate_side(side)
    order_type = validate_order_type(order_type)
    quantity = validate_quantity(quantity)
    price = validate_price(price, order_type)

    # ── 2. Build request parameters ────────────────────────────────
    params: dict = {
        "symbol": symbol,
        "side": side,
        "type": order_type,
        "quantity": quantity,
    }

    if order_type == "LIMIT":
        params["price"] = price
        params["timeInForce"] = "GTC"

    logger.debug("Placing order – request params: %s", params)

    # ── 3. Execute API call ─────────────────────────────────────────
    try:
        client = get_client()
        response = client.futures_create_order(**params)
        logger.debug("Order placed successfully – full API response: %s", response)

    except BinanceAPIException as exc:
        logger.error(
            "Binance API error [%s]: %s", exc.status_code, exc.message
        )
        raise BinanceAPIException(
            response=None,
            status_code=exc.status_code,
            message=f"Binance API error: {exc.message}",
        ) from exc

    except (ConnectionError, Timeout) as exc:
        logger.error("Network error while placing order: %s", exc)
        raise ConnectionError(
            f"Network error: unable to reach Binance API – {exc}"
        ) from exc

    # ── 4. Return clean response ────────────────────────────────────
    clean = {
        "orderId": response.get("orderId"),
        "symbol": response.get("symbol"),
        "side": response.get("side"),
        "type": response.get("type"),
        "status": response.get("status"),
        "executedQty": response.get("executedQty", "0"),
        "avgPrice": response.get("avgPrice", "0"),
    }

    logger.info(
        "Order %s placed: %s %s %s qty=%s",
        clean["orderId"],
        clean["type"],
        clean["side"],
        clean["symbol"],
        clean["executedQty"],
    )
    return clean
