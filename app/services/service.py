from datetime import date
from typing import Dict, List

from app.db.schema import TradeCreate, TradeResponse


class TradeStoreService:
    def __init__(self):
        self._trades: Dict[str, List[TradeResponse]] = {}

    def save_trade(self, trade: TradeCreate) -> TradeResponse:
        existing_versions = self._trades.get(trade.trade_id, [])

        if existing_versions:
            latest = max(existing_versions, key=lambda t: t.version)

            if trade.version < latest.version:
                raise ValueError(
                    f"Trade {trade.trade_id} has a lower version "
                    f"({trade.version}) than the stored version ({latest.version})."
                )

        if trade.maturity_date < date.today():
            raise ValueError(
                f"Trade {trade.trade_id} has a maturity date in the past: "
                f"{trade.maturity_date}."
            )

        response = TradeResponse(
            trade_id=trade.trade_id,
            version=trade.version,
            counter_party_id=trade.counter_party_id,
            portfolio_id=trade.portfolio_id,
            maturity_date=trade.maturity_date,
            created_date=date.today(),
            expired=False,
        )

        same_version = [
            t for t in existing_versions if t.version == trade.version
        ]

        if same_version:
            existing_versions.remove(same_version[0])

        existing_versions.append(response)
        self._trades[trade.trade_id] = existing_versions

        return response

    def get_latest_trade(self, trade_id: str) -> TradeResponse | None:
        versions = self._trades.get(trade_id, [])

        if not versions:
            return None

        return max(versions, key=lambda t: t.version)

    def get_all_versions(self, trade_id: str) -> List[TradeResponse]:
        return sorted(
            self._trades.get(trade_id, []),
            key=lambda t: t.version,
        )

    def expire_matured_trades(self) -> int:
        expired_count = 0
        today = date.today()

        for versions in self._trades.values():
            for trade in versions:
                if trade.maturity_date < today and not trade.expired:
                    trade.expired = True
                    expired_count += 1

        return expired_count