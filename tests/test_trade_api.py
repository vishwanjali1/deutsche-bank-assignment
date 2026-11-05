from datetime import date, timedelta

def create_trade(client, trade_id="T1", version=1):
    return client.post(
        "/trades", 
        json={
            "tradeId": trade_id,
            "version": version,
            "counterPartyId": "CP-1",
            "portfolioId": "B1",
            "maturityDate": str(date.today() + timedelta(days=10)),
        }
    )

def test_create_trade_returns_201(client):
    response = create_trade(client)

    assert response.status_code == 201
    body = response.json()
    assert body["tradeId"] == "T1"
    assert body["version"] == 1
    assert body["expired"] is False

def test_lower_version_returns_409(client):
    create_trade(client, version=2)

    response = create_trade(client, version=1)

    assert response.status_code == 409
    assert "lower version" in response.json()["detail"].lower()

def test_same_version_replaces_trade(client):
    create_trade(client, version=1)

    response = client.post(
        "/trades",
        json={
            "tradeId": "T1",
            "version": 1,
            "counterPartyId": "CP-9",
            "portfolioId": "B9",
            "maturityDate": str(date.today() + timedelta(days=30)),
        },
    )

    assert response.status_code == 200

    latest = client.get("/trades/T1").json()
    assert latest["counterPartyId"] == "CP-9"
    assert latest["portfolioId"] == "B9"

def test_past_maturity_date_returns_422(client):
    response = client.post(
        "/trades",
        json={
            "tradeId": "T2",
            "version": 1,
            "counterPartyId": "CP-1",
            "portfolioId": "B1",
            "maturityDate": str(date.today() - timedelta(days=1)),
        },
    )

    assert response.status_code == 422


def test_get_missing_trade_returns_404(client):
    response = client.get("/trades/UNKNOWN")

    assert response.status_code == 404