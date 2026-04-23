from datetime import date as datetime_date
from sqlmodel import SQLModel, Field, Relationship


class Company(SQLModel, table=True):
    __tablename__ = "companies"

    id: int | None = Field(default=None, primary_key=True)
    symbol: str = Field(unique=True, index=True)
    name: str
    sector: str

    stocks: list["StockData"] = Relationship(back_populates="company", cascade_delete=True)


class StockData(SQLModel, table=True):
    __tablename__ = "stock_data"

    id: int | None = Field(default=None, primary_key=True)
    company_id: int = Field(foreign_key="companies.id", index=True)
    date: datetime_date = Field(index=True)
    open: float
    high: float
    low: float
    close: float
    volume: int
    daily_return: float
    moving_avg_7d: float | None = None
    high_52w: float
    low_52w: float
    volatility_score: float | None = None

    company: Company = Relationship(back_populates="stocks")
