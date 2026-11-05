from datetime import date

from sqlalchemy import Boolean, Date, Integer, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from app.db.database import Base


class Trade(Base):
    __tablename__ = "trades"
    #__table_args__ = (
    #    UniqueConstraint("trade_id", name="uq_trade_id_version"),
    #)

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    trade_id: Mapped[str] = mapped_column(String(50), index=True)
    version: Mapped[int] = mapped_column(Integer)
    counter_party_id: Mapped[str] = mapped_column(String(50))
    portfolio_id: Mapped[str] = mapped_column(String(50))
    maturity_date: Mapped[date] = mapped_column(Date)
    created_date: Mapped[date] = mapped_column(Date)
    expired: Mapped[bool] = mapped_column(Boolean, default=False)