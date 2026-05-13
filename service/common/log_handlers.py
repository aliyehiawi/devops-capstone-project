"""
Log Handlers
"""
import logging


def init_logging(app, logger_name: str):
    """Set up logging for production"""
    app.logger.propagate = False
    gunicorn_logger = logging.getLogger(logger_name)
    if gunicorn_logger:
        app.logger.handlers = gunicorn_logger.handlers
        app.logger.setLevel(gunicorn_logger.level)
    for handler in app.logger.handlers:
        formatter = logging.Formatter(
            "[%(asctime)s] [%(levelname)s] [%(module)s] %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S %z",
        )
        handler.setFormatter(formatter)
    app.logger.info("Logging handler established")
