
from datetime import date

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    Response,
    status,
)
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.db.models import Trade
from app.db.schema import TradeCreate, TradeResponse

router = APIRouter(prefix="/trades", tags=["Trades"])


@router.post("", response_model=TradeResponse)
def create_trade(
    trade: TradeCreate,
    response: Response,
    db: Session = Depends(get_db),
):
    existing_versions = (
        db.query(Trade)
        .filter(Trade.trade_id == trade.trade_id)
        .all()
    )

    # Validate trade version
    if existing_versions:
        latest = max(existing_versions, key=lambda t: t.version)

        if trade.version < latest.version:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=(
                    f"Trade {trade.trade_id} has a lower version "
                    f"({trade.version}) than stored version "
                    f"({latest.version})."
                ),
            )

    # Validate maturity date
    if trade.maturity_date < date.today():
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Maturity date cannot be earlier than today's date.",
        )

    # Check whether this version already exists
    same_version = next(
        (
            t for t in existing_versions
            if t.version == trade.version
        ),
        None,
    )

    if same_version:
        # Replace existing trade version
        db.delete(same_version)
        response.status_code = status.HTTP_200_OK
    else:
        # New trade creation
        response.status_code = status.HTTP_201_CREATED

    db_trade = Trade(
        trade_id=trade.trade_id,
        version=trade.version,
        counter_party_id=trade.counter_party_id,
        portfolio_id=trade.portfolio_id,
        maturity_date=trade.maturity_date,
        created_date=date.today(),
        expired=False,
    )

    db.add(db_trade)
    db.commit()
    db.refresh(db_trade)

    return db_trade


@router.get("/{trade_id}", response_model=TradeResponse)
def get_latest_trade(
    trade_id: str,
    db: Session = Depends(get_db),
):
    trade = (
        db.query(Trade)
        .filter(Trade.trade_id == trade_id)
        .order_by(Trade.version.desc())
        .first()
    )

    if not trade:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Trade {trade_id} not found.",
        )

    return trade


@router.get("/{trade_id}/versions",
            response_model=list[TradeResponse])
def get_trade_versions(
    trade_id: str,
    db: Session = Depends(get_db),
):
    trades = (
        db.query(Trade)
        .filter(Trade.trade_id == trade_id)
        .order_by(Trade.version.asc())
        .all()
    )

    if not trades:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Trade {trade_id} not found.",
        )

    return trades


@router.get("", response_model=list[TradeResponse])
def list_trades(db: Session = Depends(get_db)):
    return (
        db.query(Trade)
        .order_by(Trade.trade_id, Trade.version)
        .all()
    )


@router.post("/expiry/run")
def run_expiry(db: Session = Depends(get_db)):
    today = date.today()

    matured_trades = (
        db.query(Trade)
        .filter(
            Trade.maturity_date < today,
            Trade.expired.is_(False),
        )
        .all()
    )

    for trade in matured_trades:
        trade.expired = True

    db.commit()

    return {"expired_count": len(matured_trades)}
