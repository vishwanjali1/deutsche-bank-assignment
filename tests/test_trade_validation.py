from datetime import date, timedelta
from app.services.service import TradeStoreService
from app.services.service import TradeCreate

def test_reject_lower_version() :
    service = TradeStoreService()

    service.save_trade(
        TradeCreate(
            trade_id="T1",
            version=2,
            counter_party_id="CP-1",
            portfolio_id="B1",
            maturity_date=date.today() + timedelta(days=10),
        )
    )

    try:
        service.save_trade(
            TradeCreate(
                trade_id="T1",
                version=1,
                counter_party_id="CP-1",
                portfolio_id="B1",
                maturity_date=date.today() + timedelta(days=20)
            )
        )

        assert False, "Lower version should be rejected"

    except ValueError as exc:
         assert "lower version" in str(exc).lower()

def test_same_version_replaces_existing_trade():

    service = TradeStoreService()

    service.save_trade(
            TradeCreate(
                trade_id="T1",
                version=2,
                counter_party_id="CP-1",
                portfolio_id="B1",
                maturity_date=date.today() + timedelta(days=10),
            )
        )

    service.save_trade(
            TradeCreate(
                trade_id="T1",
                version=2,
                counter_party_id="CP-2",
                portfolio_id="B2",
                maturity_date=date.today() + timedelta(days=20),
        )
    )

    trade = service.get_latest_trade("T1")
    assert "CP-2" == trade.counter_party_id
    assert "B2" == trade.portfolio_id

def test_reject_past_maturity_date() :

    service = TradeStoreService()

    try: 
        service.save_trade(
                    TradeCreate(
                        trade_id="T1",
                        version=1,
                        counter_party_id="CP-1",
                        portfolio_id="B1",
                        maturity_date=date.today() - timedelta(days=1),
                    )
                )

        assert False, "Past maturity date should be rejected"

    except ValueError as exc:
        "Maturity date" in str(exc).lower()

def test_higher_version_is_accepted() :

    service = TradeStoreService()

    service.save_trade(
            TradeCreate(
                            trade_id="T1",
                            version=1,
                            counter_party_id="CP-1",
                            portfolio_id="B1",
                            maturity_date=date.today() + timedelta(days=10),
                        )
                    )

    service.save_trade(
                TradeCreate(
                                trade_id="T1",
                                version=2,
                                counter_party_id="CP-1",
                                portfolio_id="B1",
                                maturity_date=date.today() + timedelta(days=15),
                            )
                        )

    trade = service.get_latest_trade("T1")
    assert trade.version == 2
    

    







    



