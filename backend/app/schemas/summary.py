from pydantic import BaseModel


class SummaryOut(BaseModel):
    """Response schema for stock summary (52-week stats)."""

    symbol: str
    name: str
    sector: str
    current_price: float
    high_52w: float
    low_52w: float
    avg_close: float
    total_return_1y: float
    volatility_score: float | None
    volume_avg: float
