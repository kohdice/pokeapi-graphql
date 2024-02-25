import logging


def configure_logging() -> None:
    """Configures the logging module."""

    log_format = (
        "[%(levelname)s] %(asctime)s - %(name)s, line: %(lineno)d - %(message)s"
    )
    logging.basicConfig(
        level=logging.DEBUG, format=log_format, datefmt="%Y-%m-%d %H:%M:%S"
    )
