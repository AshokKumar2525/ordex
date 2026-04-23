"""
Binance Client Wrapper (Testnet).

Initialises a ``python-binance`` client configured to communicate with
the Binance Futures **Testnet** (https://testnet.binancefuture.com).

API credentials are loaded from environment variables via ``python-dotenv``.
"""

import logging
import os

from dotenv import load_dotenv
from binance.client import Client

# Load .env from the project root (one level above bot/)
load_dotenv(
    dotenv_path=os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))), ".env"
    )
)

logger = logging.getLogger(__name__)

# Module-level singleton – lazily initialised by get_client()
_client: Client | None = None


def get_client() -> Client:
    """
    Return a singleton Binance Futures Testnet client.

    On the first call the client is created using ``API_KEY`` and
    ``API_SECRET`` from the environment.  Subsequent calls return the
    same instance.

    Returns:
        binance.client.Client: An authenticated testnet client.

    Raises:
        EnvironmentError: If ``API_KEY`` or ``API_SECRET`` are missing.
    """
    global _client  # noqa: PLW0603

    if _client is not None:
        return _client

    api_key = os.getenv("API_KEY")
    api_secret = os.getenv("API_SECRET")

    if not api_key or not api_secret:
        raise EnvironmentError(
            "Missing API credentials. Set API_KEY and API_SECRET in your .env file."
        )

    _client = Client(
        api_key=api_key,
        api_secret=api_secret,
        testnet=True,
    )

    # Point futures endpoints to the testnet
    _client.FUTURES_URL = "https://testnet.binancefuture.com/fapi"

    logger.debug(
        "Binance Futures Testnet client initialised successfully "
        "(base URL: https://testnet.binancefuture.com)"
    )
    return _client
