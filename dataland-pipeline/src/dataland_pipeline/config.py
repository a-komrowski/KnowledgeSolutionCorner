from pathlib import Path
from pydantic import BaseModel
from dotenv import load_dotenv
import os

load_dotenv()

class Settings(BaseModel):
    base_url_api: str = "https://dataland.com/api"
    base_url_documents: str = "https://dataland.com/documents"
    api_token: str | None = os.getenv("DATALAND_TOKEN")
    company_query: str = "Siemens"

    timeout_search: int = 30
    timeout_data: int = 20
    timeout_values: int = 30
    max_retries: int = 3
    backoff_base: int = 2
    backoff_max: int = 60
    rate_limit_wait: int = 60

    raw_dir: Path = Path("data/raw")

    def ensure_dirs(self):
        self.raw_dir.mkdir(parents=True, exist_ok=True)

settings = Settings()
settings.ensure_dirs()
