"""
tests/test_logging.py


Basic logging structure
"""

import pytest
import logging
from enum import Enum


# Define LogLevel Enum
class LogLevel(Enum):
    DEBUG = logging.DEBUG
    INFO = logging.INFO
    WARNING = logging.WARNING
    ERROR = logging.ERROR
    CRITICAL = logging.CRITICAL
    EMERGENCY = 60


# Register the custom log levels with logging module
logging.addLevelName(LogLevel.EMERGENCY.value, "EMERGENCY")


# Create custom emergency function tp use with logging.
def emergency(self, message, *args, **kwargs):
    if self.isEnabledFor(LogLevel.EMERGENCY.value):
        self._log(LogLevel.EMERGENCY.value, message, args, **kwargs)


# Attach function to Logger class
logging.Logger.emergency = emergency


def custom_logger(name: str, level: LogLevel) -> logging.Logger:
    # Create a named logger
    logger = logging.getLogger(name)
    logger.setLevel(level.value)  # Set logger level using enum value

    # Create a console handler and set its level
    console_handler = logging.StreamHandler()
    console_handler.setLevel(level.value)

    # Create a file handler and set its level
    file_handler = logging.FileHandler(f"{name}.log")
    file_handler.setLevel(level.value)

    # Set the formatter for the console and file handlers
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%m/%d/%Y %I:%M:%S%p",
    )
    console_handler.setFormatter(formatter)
    file_handler.setFormatter(formatter)

    # Add both handlers to the logger
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    return logger


@pytest.mark.logging
class TestLogging:
    # Example usage
    logger = custom_logger("custom_logger", LogLevel.DEBUG)

    def test_default_logger(self):
        logging.debug(f"Running inside class - {__class__}")
        logging.info("This is a simple log message")

    def test_custom_logger(self):
        # Logging messages with different levels
        self.logger.debug("This is a DEBUG level message.")
        self.logger.info("This is an INFO level message.")
        self.logger.warning("This is a WARNING level message.")
        self.logger.error("This is an ERROR level message.")
        self.logger.critical("This is a CRITICAL level message.")
        self.logger.emergency("This is an EMERGENCY level message.")
