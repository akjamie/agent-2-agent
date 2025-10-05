import logging
import os
from logging.handlers import RotatingFileHandler
import traceback

class LogUtil:
    _logger = None
    _log_file = None
    _max_bytes = 5 * 1024 * 1024  # 5MB
    _backup_count = 5

    @classmethod
    def get_logger(cls, name: str = "app"):
        if cls._logger is None:
            log_dir = os.path.join(os.path.dirname(__file__), "..", "..", "logs")
            os.makedirs(log_dir, exist_ok=True)
            cls._log_file = os.path.join(log_dir, "app.log")

            logger = logging.getLogger(name)
            logger.setLevel(logging.INFO)
            formatter = logging.Formatter('[%(asctime)s] %(levelname)s %(name)s: %(message)s')

            # Avoid duplicate handlers
            if not logger.hasHandlers():
                # Rotating file handler
                fh = RotatingFileHandler(cls._log_file, maxBytes=cls._max_bytes, backupCount=cls._backup_count)
                fh.setFormatter(formatter)
                logger.addHandler(fh)

                # Console handler
                ch = logging.StreamHandler()
                ch.setFormatter(formatter)
                logger.addHandler(ch)

            cls._logger = logger
        return cls._logger

    @classmethod
    def set_level(cls, level):
        cls.get_logger().setLevel(level)

    @classmethod
    def info(cls, msg):
        cls.get_logger().info(msg)

    @classmethod
    def error(cls, msg, exc: Exception = None):
        if exc:
            msg = f"{msg}\n{traceback.format_exc()}"
        cls.get_logger().error(msg)

    @classmethod
    def warning(cls, msg):
        cls.get_logger().warning(msg)

    @classmethod
    def debug(cls, msg):
        cls.get_logger().debug(msg)

    @classmethod
    def exception(cls, msg):
        cls.get_logger().exception(msg)

    @classmethod
    def log(cls, level, msg):
        cls.get_logger().log(level, msg)

# Usage example:
# LogUtil.info("Info message")
# LogUtil.error("Error message", exc=Exception("Test error"))
# LogUtil.set_level(logging.DEBUG)
