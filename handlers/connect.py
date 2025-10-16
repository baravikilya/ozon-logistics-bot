"""
Ozon connection handler for Ozon Logistics Bot.
Handles connecting Ozon Seller API credentials (stub implementation).
"""

from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

router = Router()


class ConnectStates(StatesGroup):
    """States for Ozon connection flow."""
    waiting_for_client_id = State()
    waiting_for_api_key = State()


@router.callback_query(F.data == "menu_connect")
async def start_connect(callback: CallbackQuery, state: FSMContext) -> None:
    """
    Start Ozon connection process.
    Ask user for Client ID.
    """
    await state.clear()  # Clear any previous state

    text = (
        "🔗 <b>Подключение Ozon Seller</b>\n\n"
        "Для подключения вашего магазина введите данные из Ozon Seller Center:\n\n"
        "Введите <b>Client ID</b> из настроек API:"
    )

    await callback.message.edit_text(text, parse_mode="HTML")
    await state.set_state(ConnectStates.waiting_for_client_id)
    await callback.answer()


@router.message(ConnectStates.waiting_for_client_id)
async def process_client_id(message: Message, state: FSMContext) -> None:
    """
    Process Client ID input and ask for API Key.
    """
    client_id = message.text.strip()

    # Basic validation (stub)
    if not client_id or len(client_id) < 10:
        await message.reply(
            "❌ <b>Ошибка:</b> Client ID должен содержать минимум 10 символов.\n"
            "Попробуйте еще раз:",
            parse_mode="HTML"
        )
        return

    # Store client_id in state
    await state.update_data(client_id=client_id)

    text = (
        "✅ Client ID принят!\n\n"
        "Теперь введите <b>API Key</b> (токен) с правами Read-Only:"
    )

    await message.reply(text, parse_mode="HTML")
    await state.set_state(ConnectStates.waiting_for_api_key)


@router.message(ConnectStates.waiting_for_api_key)
async def process_api_key(message: Message, state: FSMContext) -> None:
    """
    Process API Key input and complete connection (stub).
    """
    api_key = message.text.strip()

    # Basic validation (stub)
    if not api_key or len(api_key) < 20:
        await message.reply(
            "❌ <b>Ошибка:</b> API Key должен содержать минимум 20 символов.\n"
            "Попробуйте еще раз:",
            parse_mode="HTML"
        )
        return

    # Get stored data
    data = await state.get_data()
    client_id = data.get("client_id")

    # Here would be actual API validation (stub for now)
    success_text = (
        "✅ <b>Данные получены!</b>\n\n"
        f"Client ID: <code>{client_id}</code>\n"
        f"API Key: <code>{'*' * len(api_key)}</code>\n\n"
        "🔄 <i>Проверка подключения... (логика будет добавлена позже)</i>\n\n"
        "Используйте /start для возврата в главное меню."
    )

    await message.reply(success_text, parse_mode="HTML")

    # Clear state
    await state.clear()

    # TODO: Save to database when implemented
    # TODO: Validate credentials with Ozon API