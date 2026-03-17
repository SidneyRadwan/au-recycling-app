from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=Path(__file__).parent / ".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # Database
    database_url: str = Field(
        default="",
        description="PostgreSQL connection string (jdbc: or plain postgres:// format)",
    )
    database_username: str = Field(default="recycling")
    database_password: str = Field(default="recycling_dev")

    # Anthropic
    anthropic_api_key: str = Field(default="")
    extraction_model: str = Field(default="claude-opus-4-6")

    # Scraper behaviour
    scraper_output_dir: Path = Field(default=Path(__file__).parent / "output")
    scraper_rate_limit: float = Field(default=1.0)

    # Seed data source URLs — override if a government directory page moves
    seed_nsw_url: str = Field(
        default="https://www.olg.nsw.gov.au/public/local-government-directory/"
    )
    seed_vic_url: str = Field(
        default="https://www.vic.gov.au/local-government-contacts-and-information"
    )
    seed_qld_url: str = Field(
        default=(
            "https://www.dlgwv.qld.gov.au/local-government/for-the-community"
            "/local-government-directory/search-the-local-government-directory"
        )
    )
    seed_qld_api_url: str = Field(
        default=(
            "https://www.dlgwv.qld.gov.au/local-government/for-the-community"
            "/local-government-directory/lg-directory-config/get-lga-json?lgacode="
        )
    )
    seed_wa_url: str = Field(default="https://mycouncil.wa.gov.au")
    seed_sa_url: str = Field(
        default="https://en.wikipedia.org/wiki/Local_government_areas_of_South_Australia"
    )
    seed_tas_url: str = Field(
        default="https://en.wikipedia.org/wiki/Local_government_areas_of_Tasmania"
    )
    seed_nt_url: str = Field(
        default=(
            "https://nt.gov.au/community/local-councils-remote-communities-and-homelands"
            "/find-your-council"
        )
    )
    seed_postcodes_url: str = Field(
        default=(
            "https://raw.githubusercontent.com/matthewproctor/"
            "australianpostcodes/master/australian_postcodes.csv"
        )
    )

    def get_database_url(self) -> str:
        if not self.database_url:
            raise EnvironmentError(
                "DATABASE_URL is not set. Copy .env.example to .env and fill in the value."
            )
        return self.database_url

    def get_anthropic_api_key(self) -> str:
        if not self.anthropic_api_key:
            raise EnvironmentError(
                "ANTHROPIC_API_KEY is not set. Copy .env.example to .env and fill in the value."
            )
        return self.anthropic_api_key


settings = Settings()
