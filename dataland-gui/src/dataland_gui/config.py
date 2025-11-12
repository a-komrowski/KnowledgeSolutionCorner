from __future__ import annotations
import os
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv(override=False)

@dataclass(frozen=True)
class Settings:
    base_url: str = os.getenv("DATALAND_BASE_URL", "https://dataland.com").rstrip("/")
    api_key_file: str = os.path.join(os.getcwd(), "apikey.txt")
    api_key_env: str | None = os.getenv("DATALAND_API_KEY")
    http_timeout: float = float(os.getenv("DATALAND_HTTP_TIMEOUT", "25"))
    port: int = int(os.getenv("PORT", "5050"))
    sfdr_show_only_active_default: bool = os.getenv("DATALAND_SFDR_ACTIVE", "true").lower() == "true"

SETTINGS = Settings()
