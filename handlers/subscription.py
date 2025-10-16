"""
Subscription management handler for Ozon Logistics Bot.
Handles subscription status display and payment options (stub implementation).
"""

from datetime import datetime, timedelta

from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder

from core.config import settings

router = Router()


@router.callback_query(F.data == "menu_subscribe")
async def show_subscription_status(callback: CallbackQuery) -> None:
    """
    Show current subscription status.
    In MVP this is a stub showing trial status.
    """
    # Mock user data (will be replaced with database query)
    trial_start = datetime.utcnow() - timedelta(days=2)  # Mock: trial started 2 days ago
    trial_end = trial_start + timedelta(days=settings.trial_period_days)
    days_left = (trial_end - datetime.utcnow()).days

    if days_left > 0:
        status_text = (
            "💳 <b>Статус подписки</b>\n\n"
            f"📅 Trial-период до: {trial_end.strftime('%d.%m.%Y')}\n"
            f"⏰ Осталось дней: {days_left}\n\n"
            "После окончания trial-периода потребуется оплата для продолжения использования."
        )
    else:
        status_text = (
            "💳 <b>Статус подписки</b>\n\n"
            "❌ Trial-период истек!\n\n"
            "Для продолжения использования необходимо оплатить подписку."
        )

    # Create subscription menu keyboard
    keyboard = InlineKeyboardBuilder()
    keyboard.button(text="💰 Оплатить / Продлить", callback_data="pay_menu")
    keyboard.button(text="🔄 Отменить автопродление", callback_data="cancel_auto_renew")  # Stub
    keyboard.button(text="⬅️ Назад", callback_data="back_to_main")

    keyboard.adjust(1)

    await callback.message.edit_text(
        status_text,
        reply_markup=keyboard.as_markup(),
        parse_mode="HTML"
    )
    await callback.answer()


@router.callback_query(F.data == "pay_menu")
async def show_payment_options(callback: CallbackQuery) -> None:
    """Show payment options menu."""
    payment_text = (
        "💰 <b>Выберите срок подписки</b>\n\n"
        f"1 месяц: {settings.subscription_price_1m} ₽\n"
        f"6 месяцев: {settings.subscription_price_6m} ₽ (скидка!)\n"
        f"1 год: {settings.subscription_price_1y} ₽ (макс. скидка!)\n\n"
        "Оплата через YooKassa (будет реализована позже)."
    )

    keyboard = InlineKeyboardBuilder()
    keyboard.button(text=f"1 месяц ({settings.subscription_price_1m} ₽)", callback_data="pay_1m")
    keyboard.button(text=f"6 месяцев ({settings.subscription_price_6m} ₽)", callback_data="pay_6m")
    keyboard.button(text=f"1 год ({settings.subscription_price_1y} ₽)", callback_data="pay_1y")
    keyboard.button(text="⬅️ Назад", callback_data="menu_subscribe")

    keyboard.adjust(1)

    await callback.message.edit_text(
        payment_text,
        reply_markup=keyboard.as_markup(),
        parse_mode="HTML"
    )
    await callback.answer()


@router.callback_query(F.data.startswith("pay_"))
async def process_payment(callback: CallbackQuery) -> None:
    """Process payment selection (stub implementation)."""
    payment_type = callback.data

    # Mock payment processing
    if payment_type == "pay_1m":
        amount = settings.subscription_price_1m
        period = "1 месяц"
    elif payment_type == "pay_6m":
        amount = settings.subscription_price_6m
        period = "6 месяцев"
    elif payment_type == "pay_1y":
        amount = settings.subscription_price_1y
        period = "1 год"
    else:
        await callback.answer("Ошибка выбора периода")
        return

    success_text = (
        f"✅ <b>Оплата инициирована!</b>\n\n"
        f"Период: {period}\n"
        f"Сумма: {amount} ₽\n\n"
        "🔄 <i>Перенаправление на YooKassa... (будет реализовано позже)</i>\n\n"
        "После оплаты подписка будет активирована автоматически."
    )

    keyboard = InlineKeyboardBuilder()
    keyboard.button(text="⬅️ Назад к подписке", callback_data="menu_subscribe")

    await callback.message.edit_text(
        success_text,
        reply_markup=keyboard.as_markup(),
        parse_mode="HTML"
    )
    await callback.answer()


@router.callback_query(F.data == "cancel_auto_renew")
async def cancel_auto_renew(callback: CallbackQuery) -> None:
    """Cancel auto-renewal (stub)."""
    text = (
        "🔄 <b>Отмена автопродления</b>\n\n"
        "<i>Функция будет реализована позже</i>\n\n"
        "Автопродление подписки отключено."
    )

    keyboard = InlineKeyboardBuilder()
    keyboard.button(text="⬅️ Назад к подписке", callback_data="menu_subscribe")

    await callback.message.edit_text(
        text,
        reply_markup=keyboard.as_markup(),
        parse_mode="HTML"
    )
    await callback.answer()


@router.callback_query(F.data == "back_to_main")
async def back_to_main(callback: CallbackQuery) -> None:
    """Go back to main menu."""
    # This will trigger the start command handler
    await callback.message.edit_text(
        "Возвращаемся в главное меню...",
        reply_markup=None
    )
    await callback.answer()