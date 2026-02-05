"""Logging configuration for different environments."""

import sys
from app.config import settings


def setup_logging() -> None:
    """Configure logging based on environment."""
    import logging.config

    log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

    if settings.environment == "production":
        # JSON structured logging for production
        try:
            from pythonjsonlogger import jsonlogger

            logging.config.dictConfig(
                {
                    "version": 1,
                    "formatters": {
                        "json": {
                            "()": "pythonjsonlogger.jsonlogger.JsonFormatter",
                            "format": "%(asctime)s %(name)s %(levelname)s %(message)s",
                        }
                    },
                    "handlers": {
                        "console": {
                            "class": "logging.StreamHandler",
                            "formatter": "json",
                            "stream": sys.stdout,
                        }
                    },
                    "root": {
                        "level": settings.log_level,
                        "handlers": ["console"],
                    },
                }
            )
        except ImportError:
            logging.basicConfig(
                level=getattr(logging, settings.log_level.upper()),
                format=log_format,
                stream=sys.stdout,
            )
    else:
        import logging

        logging.basicConfig(
            level=getattr(logging, settings.log_level.upper()),
            format=log_format,
            stream=sys.stdout,
        )
