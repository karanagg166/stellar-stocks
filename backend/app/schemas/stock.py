from datetime import date

from pydantic import BaseModel


class StockDataOut(BaseModel):
    """Response schema for a single stock data record."""

    date: date
    open: float
    high: float
    low: float
    close: float
    volume: int
    daily_return: float
    moving_avg_7d: float | None
    high_52w: float
    low_52w: float
    volatility_score: float | None

    model_config = {"from_attributes": True}


class StockDataListOut(BaseModel):
    """Response schema for the stock data endpoint."""

    symbol: str
    name: str
    days: int
    data: list[StockDataOut]
