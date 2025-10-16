"""
Start command handler for Ozon Logistics Bot.
Handles /start command and main menu navigation.
"""

from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder

from core.db import get_user_by_telegram_id, create_user
from core.config import settings

router = Router()


@router.message(Command("start"))
async def cmd_start(message: Message) -> None:
    """
    Handle /start command.
    Create user if doesn't exist and show welcome message with main menu.
    """
    telegram_id = message.from_user.id

    # Get or create user
    async for session in get_db():
        user = await get_user_by_telegram_id(session, telegram_id)
        if not user:
            user = await create_user(session, telegram_id)

    # Welcome message
    welcome_text = (
        "🚚 <b>Ozon Logistics Bot</b>\n\n"
        "Ваш помощник в анализе логистики Ozon!\n\n"
        "📹 <i>Видео-инструкция будет добавлена позже</i>\n\n"
        "Выберите действие:"
    )

    # Create main menu keyboard
    keyboard = InlineKeyboardBuilder()
    keyboard.button(text="🔗 Подключить Ozon", callback_data="menu_connect")
    keyboard.button(text="💳 Моя Подписка", callback_data="menu_subscribe")
    keyboard.button(text="📊 Получить Отчет", callback_data="menu_report")
    keyboard.button(text="🆘 Поддержка", url="https://t.me/support")  # Placeholder URL

    keyboard.adjust(1)  # One button per row

    await message.reply(
        welcome_text,
        reply_markup=keyboard.as_markup(),
        parse_mode="HTML"
    )


@router.callback_query(F.data == "menu_connect")
async def menu_connect(callback: CallbackQuery) -> None:
    """Handle main menu -> Connect Ozon button."""
    await callback.message.edit_text(
        "Переходим к подключению Ozon...",
        reply_markup=None
    )
    # This will be handled by connect.py handler
    await callback.answer()


@router.callback_query(F.data == "menu_subscribe")
async def menu_subscribe(callback: CallbackQuery) -> None:
    """Handle main menu -> Subscription button."""
    await callback.message.edit_text(
        "Переходим к управлению подпиской...",
        reply_markup=None
    )
    # This will be handled by subscription.py handler
    await callback.answer()


@router.callback_query(F.data == "menu_report")
async def menu_report(callback: CallbackQuery) -> None:
    """Handle main menu -> Get Report button."""
    await callback.message.edit_text(
        "Переходим к генерации отчета...",
        reply_markup=None
    )
    # This will be handled by report.py handler
    await callback.answer()


# Helper function (will be moved to proper location later)
async def get_db():
    """Temporary helper - will be replaced with proper dependency injection."""
    from core.db import async_session
    async with async_session() as session:
        yield session