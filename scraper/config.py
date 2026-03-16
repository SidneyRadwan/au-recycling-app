import os
from pathlib import Path

from dotenv import load_dotenv

_here = Path(__file__).parent
load_dotenv(_here / ".env", override=False)


def get_database_url() -> str:
    url = os.environ.get("DATABASE_URL", "")
    if not url:
        raise EnvironmentError(
            "DATABASE_URL environment variable is not set. "
            "Copy .env.example to .env and fill in the value."
        )
    return url


def get_output_dir() -> Path:
    raw = os.environ.get("SCRAPER_OUTPUT_DIR", str(_here / "output"))
    path = Path(raw)
    path.mkdir(parents=True, exist_ok=True)
    return path


def get_rate_limit() -> float:
    try:
        return float(os.environ.get("SCRAPER_RATE_LIMIT", "1.0"))
    except ValueError:
        return 1.0


def get_anthropic_api_key() -> str:
    key = os.environ.get("ANTHROPIC_API_KEY", "")
    if not key:
        raise EnvironmentError(
            "ANTHROPIC_API_KEY environment variable is not set. "
            "Copy .env.example to .env and fill in the value."
        )
    return key


def get_extraction_model() -> str:
    return os.environ.get("EXTRACTION_MODEL", "claude-opus-4-6")


class _Settings:
    @property
    def database_url(self) -> str:
        return get_database_url()

    @property
    def scraper_output_dir(self) -> Path:
        return get_output_dir()

    @property
    def rate_limit(self) -> float:
        return get_rate_limit()

    @property
    def anthropic_api_key(self) -> str:
        return get_anthropic_api_key()

    @property
    def extraction_model(self) -> str:
        return get_extraction_model()


settings = _Settings()
