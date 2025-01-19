import logging
import sys


class Logger:
    def __init__(self, name: str):
        formatter = logging.Formatter("[%(name)s] %(message)s")

        handler = logging.StreamHandler(stream=sys.stdout)
        handler.setFormatter(formatter)

        self.logger = logging.getLogger(f"{name}.stdout")
        self.logger.setLevel(logging.DEBUG)
        self.logger.addHandler(handler)

        error_handler = logging.StreamHandler(stream=sys.stderr)
        error_handler.setFormatter(formatter)

        self.error_logger = logging.getLogger(f"{name}.stderr")
        self.error_logger.setLevel(logging.DEBUG)
        self.error_logger.addHandler(error_handler)

    @property
    def debug(self):
        return self.error_logger.debug

    @property
    def info(self):
        return self.logger.info

    @property
    def warning(self):
        return self.error_logger.warning

    @property
    def error(self):
        return self.error_logger.error

    @property
    def critical(self):
        return self.error_logger.critical
