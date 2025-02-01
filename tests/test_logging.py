"""
tests/test_logging.py


Basic logging structure
"""

import pytest
import logging


class CustomLogger(logging.Logger):
    class CustomFormatter(logging.Formatter):
        grey = "\x1b[38;20m"
        yellow = "\x1b[33;20m"
        red = "\x1b[31;20m"
        bold_red = "\x1b[31;1m"
        reset = "\x1b[0m"
        format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s (%(filename)s:%(lineno)d)"
        FORMATS = {
            logging.DEBUG: grey + format + reset,
            logging.INFO: grey + format + reset,
            logging.WARNING: yellow + format + reset,
            logging.ERROR: red + format + reset,
            logging.CRITICAL: bold_red + format + reset,
        }

        def format(self, record):
            log_fmt = self.FORMATS.get(record.levelno)
            formatter = logging.Formatter(log_fmt)
            return formatter.format(record)

    def __init__(self, name, level=logging.DEBUG):
        super().__init__(name, level)
        handler = logging.StreamHandler()
        handler.setFormatter(self.CustomFormatter())
        self.addHandler(handler)


@pytest.mark.logging
class TestLogging:
    def test_default_logger(self):
        default_logger = logging.getLogger("default_logger")
        default_logger.debug(f"Running inside class - {__class__}")
        default_logger.info("This is a simple log message")

    def test_custom_logger(self):
        custom_logger = CustomLogger(name="custom_logger")
        custom_logger.debug("This is a DEBUG level message.")
        custom_logger.info("This is an INFO level message.")
        custom_logger.warning("This is a WARNING level message.")
        custom_logger.error("This is an ERROR level message.")
        custom_logger.critical("This is a CRITICAL level message.")
