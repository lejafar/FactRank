import logging
from logging.handlers import RotatingFileHandler
from logging import handlers
import sys

def init_package_logger(options):
    # we give our package logger the package name
    package_logger = logging.getLogger(__name__.split('.')[0])

    logging_formatter = logging.Formatter(f"[{options.run}][%(asctime)s-%(levelname)s %(name)s] %(message)s")

    # log to stdout
    stdout_handler = logging.StreamHandler(sys.stdout)
    stdout_handler.setFormatter(logging_formatter)
    stdout_handler.setLevel(logging._nameToLevel.get(options.log_level))
    package_logger.addHandler(stdout_handler)

    # log to file
    log_filename = options.run_path / f'{options.run}.log'
    file_handler = handlers.RotatingFileHandler(log_filename, mode='a+', encoding='utf-8', maxBytes=(1048576*5), backupCount=7)
    file_handler.setFormatter(logging_formatter)
    file_handler.setLevel(logging._nameToLevel.get(options.log_level))
    package_logger.addHandler(file_handler)

    package_logger.setLevel(logging._nameToLevel.get(options.log_level))

    return package_logger
