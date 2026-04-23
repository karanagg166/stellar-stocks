from pydantic import BaseModel

from app.schemas.stock import StockDataOut


class CompareOut(BaseModel):
    """Response schema for the /compare endpoint."""

    symbol1: str
    symbol1_name: str
    symbol2: str
    symbol2_name: str
    symbol1_data: list[StockDataOut]
    symbol2_data: list[StockDataOut]
    correlation: float | None
