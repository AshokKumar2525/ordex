"""
Logging Configuration Module.

Configures dual-handler logging for the trading bot:
  - Console handler at INFO level for user-facing output.
  - Rotating file handler at DEBUG level for detailed diagnostics.

Log files are stored in the `logs/` directory, automatically created
at runtime if it doesn't exist.
"""

import logging
import os
from logging.handlers import RotatingFileHandler

# Constants
LOG_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "logs")
LOG_FILE = os.path.join(LOG_DIR, "ordex.log")
MAX_LOG_BYTES = 5 * 1024 * 1024  # 5 MB
BACKUP_COUNT = 3

CONSOLE_FORMAT = "%(levelname)s | %(message)s"
FILE_FORMAT = "%(asctime)s | %(levelname)s | %(module)s | %(message)s"


def setup_logging() -> logging.Logger:
    """
    Configure and return the root logger with dual handlers.

    Creates the ``logs/`` directory if it does not already exist.

    Returns:
        logging.Logger: The configured root logger instance.

    Handlers:
        - **Console** – streams INFO-and-above messages with a compact format.
        - **File** – writes DEBUG-and-above messages to a rotating log file
          (``logs/ordex.log``, 5 MB per file, 3 backups).
    """
    # Ensure log directory exists
    os.makedirs(LOG_DIR, exist_ok=True)

    # Grab root logger and set to lowest level we care about
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    # Avoid adding duplicate handlers on repeated calls
    if logger.handlers:
        return logger

    # ── Console Handler (INFO) ──────────────────────────────────────
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(logging.Formatter(CONSOLE_FORMAT))

    # ── File Handler (DEBUG, rotating) ──────────────────────────────
    file_handler = RotatingFileHandler(
        LOG_FILE,
        maxBytes=MAX_LOG_BYTES,
        backupCount=BACKUP_COUNT,
        encoding="utf-8",
    )
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(logging.Formatter(FILE_FORMAT))

    # Attach handlers
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    logger.debug("Logging initialised – console=INFO, file=DEBUG (%s)", LOG_FILE)
    return logger
