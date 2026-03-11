import os
from pathlib import Path

from dotenv import load_dotenv

# Load .env from the scraper directory (or parent if not found)
_here = Path(__file__).parent
load_dotenv(_here / ".env", override=False)
load_dotenv(_here / ".env.local", override=False)


def get_database_url() -> str:
    """Return the PostgreSQL connection string.  Raises if not configured."""
    url = os.environ.get("DATABASE_URL", "")
    if not url:
        raise EnvironmentError(
            "DATABASE_URL environment variable is not set. "
            "Copy .env.example to .env and fill in the value."
        )
    return url


def get_output_dir() -> Path:
    """Return the directory where JSON output files are written."""
    raw = os.environ.get("SCRAPER_OUTPUT_DIR", str(_here / "output"))
    path = Path(raw)
    path.mkdir(parents=True, exist_ok=True)
    return path


def get_rate_limit() -> float:
    """Return the minimum seconds to sleep between HTTP requests."""
    try:
        return float(os.environ.get("SCRAPER_RATE_LIMIT", "1.0"))
    except ValueError:
        return 1.0


class _Settings:
    """Lazy settings object — values are read from environment on first access."""

    @property
    def database_url(self) -> str:
        return get_database_url()

    @property
    def scraper_output_dir(self) -> Path:
        return get_output_dir()

    @property
    def rate_limit(self) -> float:
        return get_rate_limit()


settings = _Settings()
