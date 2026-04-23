"""
Input Validation Module.

Provides strict validation for every user-supplied parameter before
an order is submitted to the Binance API. Each validator raises a
``ValueError`` with a clear, human-readable message on failure.
"""


def validate_symbol(symbol: str) -> str:
    """
    Validate a trading-pair symbol.

    Rules:
        - Must be a non-empty uppercase string.
        - Must end with ``USDT``.

    Args:
        symbol: The trading pair (e.g. ``"BTCUSDT"``).

    Returns:
        The validated (uppercased) symbol string.

    Raises:
        ValueError: If the symbol is empty, not a string, or does not
            end with ``USDT``.
    """
    if not isinstance(symbol, str) or not symbol.strip():
        raise ValueError("Symbol must be a non-empty string (e.g. 'BTCUSDT').")

    symbol = symbol.strip().upper()
    if not symbol.endswith("USDT"):
        raise ValueError(
            f"Invalid symbol '{symbol}'. Symbol must end with 'USDT' (e.g. 'BTCUSDT')."
        )
    return symbol


def validate_side(side: str) -> str:
    """
    Validate the order side.

    Accepts ``"BUY"`` or ``"SELL"`` (case-insensitive) and normalises
    the value to uppercase.

    Args:
        side: The order side.

    Returns:
        The normalised side (``"BUY"`` or ``"SELL"``).

    Raises:
        ValueError: If the side is not ``"BUY"`` or ``"SELL"``.
    """
    if not isinstance(side, str) or not side.strip():
        raise ValueError("Side must be 'BUY' or 'SELL'.")

    side = side.strip().upper()
    if side not in ("BUY", "SELL"):
        raise ValueError(
            f"Invalid side '{side}'. Must be 'BUY' or 'SELL'."
        )
    return side


def validate_order_type(order_type: str) -> str:
    """
    Validate the order type.

    Accepts ``"MARKET"`` or ``"LIMIT"`` (case-insensitive) and
    normalises to uppercase.

    Args:
        order_type: The order type.

    Returns:
        The normalised order type.

    Raises:
        ValueError: If the order type is not ``"MARKET"`` or ``"LIMIT"``.
    """
    if not isinstance(order_type, str) or not order_type.strip():
        raise ValueError("Order type must be 'MARKET' or 'LIMIT'.")

    order_type = order_type.strip().upper()
    if order_type not in ("MARKET", "LIMIT"):
        raise ValueError(
            f"Invalid order type '{order_type}'. Must be 'MARKET' or 'LIMIT'."
        )
    return order_type


def validate_quantity(quantity: float) -> float:
    """
    Validate the order quantity.

    Args:
        quantity: The quantity to trade.

    Returns:
        The validated quantity as a positive float.

    Raises:
        ValueError: If the quantity is not a positive number.
    """
    try:
        quantity = float(quantity)
    except (TypeError, ValueError) as exc:
        raise ValueError(
            f"Quantity must be a positive number, got '{quantity}'."
        ) from exc

    if quantity <= 0:
        raise ValueError(
            f"Quantity must be positive, got {quantity}."
        )
    return quantity


def validate_price(price, order_type: str) -> float | None:
    """
    Validate the price parameter.

    For ``LIMIT`` orders the price is **required** and must be positive.
    For ``MARKET`` orders the price is ignored (returns ``None``).

    Args:
        price: The limit price (may be ``None`` for market orders).
        order_type: Already-validated order type (``"MARKET"`` / ``"LIMIT"``).

    Returns:
        The validated price as a ``float``, or ``None`` for market orders.

    Raises:
        ValueError: If a LIMIT order is missing a price or the price is
            not a positive number.
    """
    if order_type == "MARKET":
        return None

    # LIMIT order – price is mandatory
    if price is None:
        raise ValueError("Price is required for LIMIT orders.")

    try:
        price = float(price)
    except (TypeError, ValueError) as exc:
        raise ValueError(
            f"Price must be a positive number, got '{price}'."
        ) from exc

    if price <= 0:
        raise ValueError(
            f"Price must be positive for LIMIT orders, got {price}."
        )
    return price
