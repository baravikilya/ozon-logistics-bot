"""
Report generation handler for Ozon Logistics Bot.
Handles report requests and period selection (stub implementation).
"""

from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder

router = Router()


@router.callback_query(F.data == "menu_report")
async def start_report_generation(callback: CallbackQuery) -> None:
    """
    Start report generation process.
    Check prerequisites and show period selection.
    """
    # Mock prerequisite checks (will be replaced with database queries)
    ozon_connected = False  # Mock: not connected
    subscription_active = True  # Mock: trial active

    if not ozon_connected:
        error_text = (
            "❌ <b>Магазин не подключен</b>\n\n"
            "Для генерации отчета необходимо:\n"
            "1. Подключить Ozon Seller API\n"
            "2. Активная подписка\n\n"
            "Используйте /start и выберите 'Подключить Ozon'"
        )
        keyboard = InlineKeyboardBuilder()
        keyboard.button(text="🔗 Подключить Ozon", callback_data="menu_connect")
        keyboard.button(text="⬅️ Назад", callback_data="back_to_main")

        await callback.message.edit_text(
            error_text,
            reply_markup=keyboard.as_markup(),
            parse_mode="HTML"
        )
        await callback.answer()
        return

    if not subscription_active:
        error_text = (
            "❌ <b>Подписка не активна</b>\n\n"
            "Для генерации отчетов требуется активная подписка.\n\n"
            "Перейдите в раздел подписки для оплаты."
        )
        keyboard = InlineKeyboardBuilder()
        keyboard.button(text="💳 Оплатить подписку", callback_data="menu_subscribe")
        keyboard.button(text="⬅️ Назад", callback_data="back_to_main")

        await callback.message.edit_text(
            error_text,
            reply_markup=keyboard.as_markup(),
            parse_mode="HTML"
        )
        await callback.answer()
        return

    # Prerequisites met, show period selection
    period_text = (
        "📊 <b>Генерация отчета</b>\n\n"
        "Выберите период для расчета продаж:\n\n"
        "✅ Магазин подключен\n"
        "✅ Подписка активна\n\n"
        "Отчет будет содержать данные о логистике и продажах."
    )

    keyboard = InlineKeyboardBuilder()
    keyboard.button(text="📅 За последние 7 дней", callback_data="set_period_7")
    keyboard.button(text="📅 За последние 28 дней", callback_data="set_period_28")
    keyboard.button(text="⬅️ Назад", callback_data="back_to_main")

    keyboard.adjust(1)

    await callback.message.edit_text(
        period_text,
        reply_markup=keyboard.as_markup(),
        parse_mode="HTML"
    )
    await callback.answer()


@router.callback_query(F.data.startswith("set_period_"))
async def process_period_selection(callback: CallbackQuery) -> None:
    """Process period selection and start report generation (stub)."""
    period_days = int(callback.data.split("_")[-1])

    processing_text = (
        f"🔄 <b>Генерация отчета</b>\n\n"
        f"Период: последние {period_days} дней\n\n"
        "📊 Сбор данных о продажах...\n"
        "🚚 Расчет логистики...\n"
        "📈 Формирование Excel-файла...\n\n"
        "<i>Отчет будет готов через несколько секунд (логика будет добавлена позже)</i>"
    )

    # Remove keyboard during processing
    await callback.message.edit_text(
        processing_text,
        reply_markup=None,
        parse_mode="HTML"
    )
    await callback.answer()

    # Mock processing delay
    # In real implementation, this would call the report service
    # await asyncio.sleep(2)

    # Mock completion
    completion_text = (
        f"✅ <b>Отчет готов!</b>\n\n"
        f"📊 Период: последние {period_days} дней\n"
        "📎 Excel-файл сгенерирован\n\n"
        "<i>Загрузка файла будет реализована позже</i>\n\n"
        "Используйте /start для новых действий."
    )

    keyboard = InlineKeyboardBuilder()
    keyboard.button(text="📊 Новый отчет", callback_data="menu_report")
    keyboard.button(text="⬅️ Главное меню", callback_data="back_to_main")

    await callback.message.edit_text(
        completion_text,
        reply_markup=keyboard.as_markup(),
        parse_mode="HTML"
    )


@router.callback_query(F.data == "back_to_main")
async def back_to_main_from_report(callback: CallbackQuery) -> None:
    """Go back to main menu from report section."""
    await callback.message.edit_text(
        "Возвращаемся в главное меню...",
        reply_markup=None
    )
    await callback.answer()