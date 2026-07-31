import logging
import os

LOG_PATH = os.environ.get("LOG_PATH", "app.log")

logger = logging.getLogger("taskmanager")
logger.setLevel(logging.INFO)

_handler = logging.FileHandler(LOG_PATH)
_formatter = logging.Formatter("%(asctime)s | %(message)s")
_handler.setFormatter(_formatter)
logger.addHandler(_handler)


def log_operation(operation: str):
    logger.info(operation)
