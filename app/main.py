from fastapi import FastAPI

from app.db.database import Base, engine
from app.routers import trades

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Trade Store API",
    version="1.0.0",
)

app.include_router(trades.router)


@app.get("/health")
def health_check():
    return {"status": "UP"}