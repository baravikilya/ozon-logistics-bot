"""
Main entry point for Ozon Logistics Bot.
Initializes FastAPI application, Telegram bot, and database.
"""

import asyncio
import logging
from contextlib import asynccontextmanager

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from fastapi import FastAPI

from core.config import settings
from core.db import create_tables
from handlers import register_handlers

# Configure logging
logging.basicConfig(
    level=getattr(logging, settings.log_level.upper()),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Global bot and dispatcher instances
bot: Bot
dp: Dispatcher


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan context manager."""
    global bot, dp

    # Startup
    logger.info("Starting Ozon Logistics Bot...")

    # Initialize bot and dispatcher
    bot = Bot(
        token=settings.telegram_bot_token,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )
    dp = Dispatcher()

    # Register all handlers
    register_handlers(dp)

    # Create database tables
    await create_tables()
    logger.info("Database tables created/verified")

    # Set webhook if URL is provided (production mode)
    if settings.telegram_webhook_url:
        webhook_url = f"{settings.telegram_webhook_url}/webhook"
        await bot.set_webhook(webhook_url)
        logger.info(f"Webhook set to: {webhook_url}")
    else:
        logger.info("Running in polling mode (development)")

    yield

    # Shutdown
    logger.info("Shutting down Ozon Logistics Bot...")
    if settings.telegram_webhook_url:
        await bot.delete_webhook()
    await bot.session.close()


# Create FastAPI application
app = FastAPI(
    title="Ozon Logistics Bot",
    description="Telegram bot for Ozon sellers logistics analytics",
    version="1.0.0",
    lifespan=lifespan
)


@app.get("/")
async def root():
    """Health check endpoint."""
    return {"status": "ok", "service": "Ozon Logistics Bot"}


@app.post("/webhook")
async def webhook_handler(update: dict):
    """Telegram webhook endpoint."""
    from aiogram.types import Update

    telegram_update = Update(**update)
    await dp.feed_update(bot, telegram_update)
    return {"status": "ok"}


async def run_polling():
    """Run bot in polling mode (for development)."""
    try:
        logger.info("Starting bot in polling mode...")
        await dp.start_polling(bot)
    except KeyboardInterrupt:
        logger.info("Bot stopped by user")
    except Exception as e:
        logger.error(f"Error in polling mode: {e}")
        raise


if __name__ == "__main__":
    # Run in development mode with polling
    asyncio.run(run_polling())