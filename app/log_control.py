import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler('./app/utilities/logs/data.log')
formatter = logging.Formatter('[%(asctime)s | %(name)s] -> [%(levelname)s]: %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
def log_info(message):
    logger.info(message)
def log_error(message):
    logger.error(message)
def log_debug(message):
    logger.debug(message)
def log_warning(message):
    logger.warning(message)
def log_critical(message):
    logger.critical(message)

# Example usage:
# log_info("This is an info message")
# log_error("This is an error message")
if __name__ == "__main__":
    log_info("Logger is set up and ready to use.")
    log_debug("This is a debug message for testing.")
    log_error("This is an error message for testing.")
    log_warning("This is a warning message for testing.")
    log_critical("This is a critical message for testing.")