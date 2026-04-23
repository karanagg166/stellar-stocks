import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    """Application configuration loaded from environment variables."""

    DATABASE_URL: str = os.getenv(
        "DATABASE_URL",
        "postgresql://stockuser:stockpass@localhost:5432/stockdb",
    )
    CORS_ORIGINS: list[str] = os.getenv(
        "CORS_ORIGINS", "http://localhost:3000"
    ).split(",")
    APP_TITLE: str = "Stock Data Intelligence Dashboard"
    APP_VERSION: str = "1.0.0"
    APP_DESCRIPTION: str = (
        "A mini financial data platform with real-time stock analytics, "
        "interactive visualizations, and comparison tools."
    )


settings = Settings()
