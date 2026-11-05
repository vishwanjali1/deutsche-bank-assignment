from datetime import date, datetime

from pydantic import BaseModel, Field, field_validator

class TradeCreate(BaseModel) :
    trade_id : str = Field(min_length=1, alias="tradeId")
    version: int = Field(ge=1)
    counter_party_id: str = Field(alias="counterPartyId", min_length=1)
    portfolio_id: str = Field(alias="portfolioId", min_length=1)
    maturity_date: date = Field(alias="maturityDate")

    model_config = {
        "populate_by_name": True,
        "json_schema_extra": {
            "example": {
                "tradeId": "T1",
                "version": 1,
                "counterPartyId": "CP-1",
                "portfolioId": "B1",
                "maturityDate": "2030-05-20"
            }
        },
    }


class TradeResponse(TradeCreate):
    created_date: date
    expired: bool

    model_config = {
        "from_attributes": True,
        "populate_by_name": True,
    }


