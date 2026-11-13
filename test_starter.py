import asyncio
import pytest
from decimal import Decimal

from starter import recommend_price


# Обычный расчёт цены
@pytest.mark.asyncio
async def test_recommend_price_success():
    async def fetch_offers():
        return {
            "status": "success",
            "offers": [
                {
                    "seller": "MYSHOP",
                    "price": Decimal("4300.00"),
                    "delivery_days": 2,
                },
                {
                    "seller": "PARTS",
                    "price": Decimal("4800.00"),
                    "delivery_days": 3,
                },
                {
                    "seller": "SLOW",
                    "price": Decimal("4700.00"),
                    "delivery_days": 8,
                },
            ],
        }

    result = await recommend_price(
        fetch_offers,
        current_price=Decimal("4900.00"),
        min_price=Decimal("4500.00"),
    )

    assert result["price"] == Decimal("4728.00")
    assert result["decision"] == "APPLY"


# Источник не отвечает вовремя
@pytest.mark.asyncio
async def test_recommend_price_timeout():
    async def fetch_offers():
        await asyncio.sleep(3)

        return {
            "status": "success",
            "offers": [],
        }

    result = await recommend_price(
        fetch_offers,
        current_price=Decimal("4900.00"),
        min_price=Decimal("4500.00"),
        timeout_s=2,
    )

    assert result["price"] == Decimal("4900.00")
    assert result["decision"] == "HOLD"