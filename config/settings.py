"""
Central configuration for Odoo AI Audit Platform.
Loads from .env and provides unified access to all settings.
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load .env file
ENV_PATH = Path(__file__).parent.parent / '.env'
load_dotenv(dotenv_path=ENV_PATH)


class Settings:
    """Application settings loaded from environment variables."""
    
    # ─── Odoo Connection ───
    ODOO_URL = os.getenv('ODOO_URL', 'http://localhost:8069')
    ODOO_DB = os.getenv('ODOO_DB', 'odoo')
    ODOO_USERNAME = os.getenv('ODOO_USERNAME', 'admin')
    ODOO_PASSWORD = os.getenv('ODOO_PASSWORD', 'admin')
    
    # ─── Database ───
    SQLITE_PATH = os.getenv('SQLITE_PATH', 'database/storage/audit.db')
    
    # ─── AI Providers ───
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', '')
    OPENAI_MODEL = os.getenv('OPENAI_MODEL', 'gpt-4')
    OLLAMA_URL = os.getenv('OLLAMA_URL', 'http://localhost:11434')
    OLLAMA_MODEL = os.getenv('OLLAMA_MODEL', 'llama3')
    
    # ─── Logging ───
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    LOG_FILE = os.getenv('LOG_FILE', 'logs/audit.log')
    
    # ─── Audit ───
    DEFAULT_AUDIT_DAYS = int(os.getenv('DEFAULT_AUDIT_DAYS', '30'))
    BATCH_SIZE = int(os.getenv('BATCH_SIZE', '1000'))
    
    @classmethod
    def to_dict(cls):
        """Return all settings as dictionary."""
        return {
            key: getattr(cls, key)
            for key in dir(cls)
            if not key.startswith('_') and key.isupper()
        }
    
    @classmethod
    def validate(cls):
        """Validate critical settings."""
        missing = []
        if not cls.ODOO_URL:
            missing.append('ODOO_URL')
        if not cls.ODOO_DB:
            missing.append('ODOO_DB')
        if not cls.OPENAI_API_KEY and not cls.OLLAMA_URL:
            missing.append('OPENAI_API_KEY or OLLAMA_URL')
        
        if missing:
            raise ValueError(f"Missing required settings: {', '.join(missing)}")
        return True


# Backward compatibility: import database/core/config/settings if exists
try:
    from database.core.config.settings import Settings as CoreSettings
    # Merge core settings
    for attr in dir(CoreSettings):
        if attr.isupper() and not hasattr(Settings, attr):
            setattr(Settings, attr, getattr(CoreSettings, attr))
except ImportError:
    pass


# Singleton instance
settings = Settings()
