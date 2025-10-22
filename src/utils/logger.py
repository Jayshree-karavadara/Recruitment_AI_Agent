import logging
import sys

def get_logger(name: str) -> logging.Logger:
    """Initializes and returns a logger with a specified name."""
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    # Create a handler to log to stdout
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging.INFO)

    # Create a formatter and add it to the handler
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    handler.setFormatter(formatter)

    # Add the handler to the logger
    logger.addHandler(handler)

    return logger