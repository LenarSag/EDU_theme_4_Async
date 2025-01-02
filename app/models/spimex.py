from datetime import datetime

from sqlalchemy import Date, DateTime, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class TradingResults(Base):
    __tablename__ = "trading_results"

    id: Mapped[int] = mapped_column(primary_key=True)
    exchange_product_id: Mapped[str]
    exchange_product_name: Mapped[str]
    oil_id: Mapped[str] = mapped_column(nullable=True)
    delivery_basis_id: Mapped[str] = mapped_column(nullable=True)
    delivery_basis_name: Mapped[str] = mapped_column(nullable=True)
    delivery_type_id: Mapped[str] = mapped_column(nullable=True)
    volume: Mapped[int] = mapped_column(nullable=True)
    total: Mapped[int] = mapped_column(nullable=True)
    count: Mapped[int] = mapped_column(nullable=True)
    date: Mapped[datetime] = mapped_column(Date, nullable=True)
    created_on: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    updated_on: Mapped[datetime] = mapped_column(
        DateTime, onupdate=func.now(), nullable=True
    )
