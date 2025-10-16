"""
Database models and session management for Ozon Logistics Bot.
"""

from datetime import datetime
from typing import Optional

from sqlalchemy import Column, Integer, String, Boolean, DateTime, BigInteger
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from .config import settings

# Create async engine
engine = create_async_engine(
    settings.database_url,
    echo=settings.debug,
    future=True,
)

# Create async session factory
async_session = sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

# Base class for all models
Base = declarative_base()


class User(Base):
    """
    User model for storing Telegram user data and Ozon API credentials.

    Fields:
    - id: Primary key
    - telegram_id: Unique Telegram user ID
    - client_id: Ozon Client ID (nullable)
    - api_key: Encrypted Ozon API Key (nullable)
    - is_active: Active subscription/trial status
    - trial_start_date: Trial period start date
    - subscription_expires_at: Subscription expiration date
    """

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    telegram_id = Column(BigInteger, unique=True, nullable=False, index=True)

    # Ozon API credentials (nullable until connected)
    client_id = Column(String, nullable=True)
    api_key = Column(String, nullable=True)  # Should be encrypted in production

    # Subscription status
    is_active = Column(Boolean, default=True, nullable=False)
    trial_start_date = Column(DateTime, default=datetime.utcnow, nullable=True)
    subscription_expires_at = Column(DateTime, nullable=True)

    def __repr__(self):
        return f"<User(id={self.id}, telegram_id={self.telegram_id}, is_active={self.is_active})>"


async def get_db() -> AsyncSession:
    """Dependency for getting async database session."""
    async with async_session() as session:
        try:
            yield session
        finally:
            await session.close()


async def create_tables():
    """Create all database tables."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def get_user_by_telegram_id(session: AsyncSession, telegram_id: int) -> Optional[User]:
    """Get user by Telegram ID."""
    result = await session.execute(
        session.query(User).filter(User.telegram_id == telegram_id)
    )
    return result.scalar_one_or_none()


async def create_user(session: AsyncSession, telegram_id: int) -> User:
    """Create new user with trial period."""
    user = User(
        telegram_id=telegram_id,
        is_active=True,
        trial_start_date=datetime.utcnow(),
    )
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return user