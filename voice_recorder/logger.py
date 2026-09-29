"""Logging setup."""

import logging
from logging.handlers import RotatingFileHandler

from . import config

_FORMAT = "%(asctime)s [%(levelname)s] %(name)s: %(message)s"


def setup_logging(level=logging.INFO, log_file=None):
    """Configure the root logger with console and rotating file output."""
    log_file = log_file or config.LOG_FILE
    log_file.parent.mkdir(parents=True, exist_ok=True)
    root = logging.getLogger()
    root.setLevel(level)
    if root.handlers:
        return
    formatter = logging.Formatter(_FORMAT)
    for handler in (
        logging.StreamHandler(),
        RotatingFileHandler(log_file, maxBytes=500_000, backupCount=2, encoding="utf-8"),
    ):
        handler.setFormatter(formatter)
        root.addHandler(handler)
