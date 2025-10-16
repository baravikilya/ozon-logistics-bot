"""
Handlers package for Telegram bot commands and callbacks.
Registers all routers with the main dispatcher.
"""

from aiogram import Dispatcher

from . import start, connect, subscription, report


def register_handlers(dp: Dispatcher) -> None:
    """
    Register all handler routers with the dispatcher.

    Args:
        dp: Aiogram Dispatcher instance
    """
    dp.include_router(start.router)
    dp.include_router(connect.router)
    dp.include_router(subscription.router)
    dp.include_router(report.router)