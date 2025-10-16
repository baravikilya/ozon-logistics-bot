"""
YooKassa payment service for Ozon Logistics Bot.
Handles payment processing and subscription management (stub implementation for MVP).
"""

from typing import Dict, Optional, Any
import httpx
from decimal import Decimal

from core.config import settings


class YooKassaService:
    """Service for interacting with YooKassa payment API."""

    def __init__(self):
        """Initialize YooKassa service."""
        self.shop_id = settings.yookassa_shop_id
        self.secret_key = settings.yookassa_secret_key
        self.base_url = "https://api.yookassa.ru/v3"

        # HTTP client for API calls
        self.client = httpx.AsyncClient(
            auth=(self.shop_id, self.secret_key),
            base_url=self.base_url,
            headers={"Content-Type": "application/json"},
            timeout=30.0
        )

    async def __aenter__(self):
        """Async context manager entry."""
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit."""
        await self.client.aclose()

    async def create_payment(
        self,
        amount: Decimal,
        currency: str = "RUB",
        description: str = "Подписка Ozon Logistics Bot",
        user_id: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Create a payment request.

        Args:
            amount: Payment amount
            currency: Currency code (default: RUB)
            description: Payment description
            user_id: Telegram user ID for metadata

        Returns:
            Payment data including payment URL
        """
        # STUB: Return mock payment data
        # TODO: Implement actual YooKassa payment creation
        return {
            "payment_id": f"mock_payment_{user_id or 'anonymous'}",
            "status": "pending",
            "amount": {
                "value": str(amount),
                "currency": currency
            },
            "description": description,
            "confirmation": {
                "type": "redirect",
                "confirmation_url": f"https://mock.yookassa.ru/pay/{user_id or 'anonymous'}"
            },
            "created_at": "2024-01-01T12:00:00Z",
            "metadata": {
                "user_id": str(user_id) if user_id else None,
                "service": "ozon_logistics_bot"
            }
        }

    async def get_payment_status(self, payment_id: str) -> Dict[str, Any]:
        """
        Get payment status by payment ID.

        Args:
            payment_id: YooKassa payment ID

        Returns:
            Payment status data
        """
        # STUB: Return mock status
        # TODO: Implement actual payment status check
        return {
            "id": payment_id,
            "status": "succeeded",  # pending, succeeded, canceled, etc.
            "amount": {
                "value": "919.00",
                "currency": "RUB"
            },
            "paid": True,
            "created_at": "2024-01-01T12:00:00Z",
            "captured_at": "2024-01-01T12:05:00Z"
        }

    async def create_subscription_payment(
        self,
        user_id: int,
        months: int,
        amount: int
    ) -> Dict[str, Any]:
        """
        Create subscription payment for specified period.

        Args:
            user_id: Telegram user ID
            months: Number of months for subscription
            amount: Payment amount in rubles

        Returns:
            Payment creation result
        """
        description = f"Подписка Ozon Logistics Bot на {months} месяц{'а' if months == 1 else 'ев'}"

        payment = await self.create_payment(
            amount=Decimal(amount),
            currency="RUB",
            description=description,
            user_id=user_id
        )

        # Add subscription metadata
        payment["subscription"] = {
            "user_id": user_id,
            "months": months,
            "amount": amount,
            "type": "subscription"
        }

        return payment

    async def process_webhook(self, webhook_data: Dict[str, Any]) -> bool:
        """
        Process YooKassa webhook notification.

        Args:
            webhook_data: Webhook payload from YooKassa

        Returns:
            bool: True if webhook processed successfully
        """
        # STUB: Mock webhook processing
        # TODO: Implement actual webhook handling with signature verification
        event_type = webhook_data.get("event")

        if event_type == "payment.succeeded":
            payment_id = webhook_data.get("object", {}).get("id")
            # TODO: Update user subscription in database
            print(f"Payment {payment_id} succeeded - subscription activated")
            return True

        return False

    async def refund_payment(
        self,
        payment_id: str,
        amount: Optional[Decimal] = None,
        reason: str = "User request"
    ) -> Dict[str, Any]:
        """
        Create refund for payment.

        Args:
            payment_id: Original payment ID
            amount: Refund amount (full refund if None)
            reason: Refund reason

        Returns:
            Refund creation result
        """
        # STUB: Mock refund
        # TODO: Implement actual refund API call
        return {
            "id": f"refund_{payment_id}",
            "payment_id": payment_id,
            "status": "succeeded",
            "amount": {
                "value": str(amount) if amount else "919.00",
                "currency": "RUB"
            },
            "created_at": "2024-01-01T12:10:00Z",
            "reason": reason
        }


# Factory function for service creation
async def create_yookassa_service() -> YooKassaService:
    """
    Create YooKassa service instance.

    Returns:
        YooKassaService instance

    Raises:
        ValueError: If YooKassa credentials are not configured
    """
    if not settings.yookassa_shop_id or not settings.yookassa_secret_key:
        raise ValueError("YooKassa credentials not configured")

    return YooKassaService()


# Utility functions for subscription pricing
def calculate_subscription_price(months: int) -> int:
    """
    Calculate subscription price based on months.

    Args:
        months: Number of months

    Returns:
        Price in rubles
    """
    if months == 1:
        return settings.subscription_price_1m
    elif months == 6:
        return settings.subscription_price_6m
    elif months == 12:
        return settings.subscription_price_1y
    else:
        # Pro-rate for other periods
        return (months * settings.subscription_price_1m * 12) // 12