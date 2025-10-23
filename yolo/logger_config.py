import logging
import logging.config
from typing import Dict, Any
from simple_settings import settings


def configure_logging() -> None:
    logging_config = get_logging_config()
    logging.config.dictConfig(logging_config)


def get_logging_config() -> Dict[str, Any]:
    return settings.LOGGING


def get_logger(name: str) -> logging.Logger:
    return logging.getLogger(name)

