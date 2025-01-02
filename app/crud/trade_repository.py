from sqlalchemy.ext.asyncio import AsyncSession

from app.models.spimex import TradingResults


async def add_trade_result(session: AsyncSession, trade_data: dict) -> None:
    new_result = TradingResults(**trade_data)
    session.add(new_result)


async def save_all(session: AsyncSession) -> None:
    await session.commit()
