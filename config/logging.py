"""
Central logging configuration for Odoo AI Audit Platform.
"""

import logging
import logging.handlers
import sys
from pathlib import Path


def setup_logging(
    level: str = "INFO",
    log_file: str = None,
    console: bool = True,
    max_bytes: int = 10_000_000,
    backup_count: int = 5
):
    """
    Setup application logging with file and console handlers.
    """
    level = level or "INFO"
    log_file = log_file or "logs/audit.log"
    
    logger = logging.getLogger('odoo_audit')
    logger.setLevel(getattr(logging, level.upper()))
    logger.handlers = []
    
    formatter = logging.Formatter(
        '%(asctime)s | %(levelname)-8s | %(name)s | %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    if console:
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)
    
    if log_file:
        log_path = Path(log_file)
        log_path.parent.mkdir(parents=True, exist_ok=True)
        
        file_handler = logging.handlers.RotatingFileHandler(
            log_file,
            maxBytes=max_bytes,
            backupCount=backup_count,
            encoding='utf-8'
        )
        file_handler.setLevel(getattr(logging, level.upper()))
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    
    return logger


def get_logger(name: str = None):
    """
    Get a child logger for a specific module.
    """
    if name:
        return logging.getLogger(f'odoo_audit.{name}')
    return logging.getLogger('odoo_audit')


# Singleton instance
logger = setup_logging()
