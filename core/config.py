"""
Configuration module for Ozon Logistics Bot.
Handles environment variables and application settings.
"""

import os
from typing import Optional
from pydantic import BaseSettings, validator


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # Telegram Bot Configuration
    telegram_bot_token: str
    telegram_webhook_url: Optional[str] = None

    # Database Configuration
    database_url: str

    # Application Settings
    debug: bool = False
    log_level: str = "INFO"

    # Trial Period Settings (days)
    trial_period_days: int = 7

    # Subscription Prices (RUB)
    subscription_price_1m: int = 990
    subscription_price_6m: int = 4990  # With discount 831 per month
    subscription_price_1y: int = 8990  # With discount 749 per month

    # YooKassa Configuration (for future use)
    yookassa_shop_id: Optional[str] = None
    yookassa_secret_key: Optional[str] = None

    # Ozon API Configuration (for future use)
    ozon_api_base_url: str = "https://api-seller.ozon.ru"

    class Config:
        env_file = ".env"
        case_sensitive = False

    @validator("database_url")
    def validate_database_url(cls, v):
        """Ensure database URL is properly formatted for asyncpg."""
        if v.startswith("postgresql://"):
            # Convert to asyncpg format
            return v.replace("postgresql://", "postgresql+asyncpg://", 1)
        elif not v.startswith("postgresql+asyncpg://"):
            raise ValueError("Database URL must be a valid PostgreSQL connection string")
        return v

    @validator("telegram_bot_token")
    def validate_bot_token(cls, v):
        """Validate Telegram bot token format."""
        if not v or len(v) < 45:
            raise ValueError("Invalid Telegram bot token")
        return v


# Global settings instance
settings = Settings()