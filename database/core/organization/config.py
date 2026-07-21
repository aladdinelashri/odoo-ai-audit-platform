import os

from dotenv import dotenv_values
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[3]
ENV_FILE = PROJECT_ROOT / ".env"

CONFIG = dotenv_values(ENV_FILE)


BUSINESS_UNIT_SOURCE = CONFIG.get(
    "BUSINESS_UNIT_SOURCE",
    "pos.category",
)
