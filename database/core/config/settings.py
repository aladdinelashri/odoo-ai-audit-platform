from dataclasses import dataclass
from pathlib import Path
import os

from dotenv import load_dotenv


# ---------------------------------------------------------
# Load .env
# ---------------------------------------------------------

ROOT = Path(__file__).resolve().parents[2]

load_dotenv(ROOT / ".env")


# ---------------------------------------------------------
# Database Settings
# ---------------------------------------------------------

@dataclass(frozen=True)
class DatabaseSettings:

    host: str
    port: int
    database: str
    user: str
    password: str


# ---------------------------------------------------------
# Global Settings
# ---------------------------------------------------------

class Settings:

    def __init__(self):

        self.database = DatabaseSettings(

            host=os.getenv("DB_HOST", ""),

            port=int(os.getenv("DB_PORT", "5432")),

            database=os.getenv("DB_NAME", ""),

            user=os.getenv("DB_USER", ""),

            password=os.getenv("DB_PASSWORD", "")

        )

    # -----------------------------------------------------

    def validate(self):

        missing = []

        if not self.database.host:
            missing.append("DB_HOST")

        if not self.database.database:
            missing.append("DB_NAME")

        if not self.database.user:
            missing.append("DB_USER")

        if not self.database.password:
            missing.append("DB_PASSWORD")

        if missing:

            raise RuntimeError(

                "Missing environment variables: "

                + ", ".join(missing)

            )


settings = Settings()

settings.validate()
