from datetime import date, timedelta

from fastapi import APIRouter, HTTPException, Query, Depends
from sqlmodel import Session, select

from app.database import get_session
from app.models import Company, StockData
from app.schemas.stock import StockDataOut, StockDataListOut

router = APIRouter()


@router.get("/data/{symbol}", response_model=StockDataListOut)
def get_stock_data(
    symbol: str,
    days: int = Query(default=30, ge=1, le=365, description="Number of days of data"),
    session: Session = Depends(get_session)
):
    """
    Returns stock data for a given symbol for the specified number of days.
    Default: last 30 days. Max: 365 days.
    """
    company = session.exec(select(Company).where(Company.symbol == symbol)).first()
    if not company:
        raise HTTPException(status_code=404, detail=f"Company '{symbol}' not found")

    cutoff_date = date.today() - timedelta(days=days)

    records = session.exec(
        select(StockData)
        .where(StockData.company_id == company.id)
        .where(StockData.date >= cutoff_date)
        .order_by(StockData.date)
    ).all()

    return StockDataListOut(
        symbol=company.symbol,
        name=company.name,
        days=days,
        data=[
            StockDataOut(
                date=r.date,
                open=r.open,
                high=r.high,
                low=r.low,
                close=r.close,
                volume=r.volume,
                daily_return=r.daily_return,
                moving_avg_7d=r.moving_avg_7d,
                high_52w=r.high_52w,
                low_52w=r.low_52w,
                volatility_score=r.volatility_score,
            )
            for r in records
        ],
    )
