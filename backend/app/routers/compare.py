from datetime import date, timedelta

from fastapi import APIRouter, HTTPException, Query, Depends
from sqlmodel import Session, select

from app.database import get_session
from app.models import Company, StockData
from app.schemas.stock import StockDataOut
from app.schemas.compare import CompareOut
from app.services.analytics_service import compute_correlation

router = APIRouter()


@router.get("/compare", response_model=CompareOut)
def compare_stocks(
    symbol1: str = Query(..., description="First stock symbol"),
    symbol2: str = Query(..., description="Second stock symbol"),
    days: int = Query(default=30, ge=1, le=365, description="Number of days"),
    session: Session = Depends(get_session)
):
    """
    Compare two stocks' performance over the specified period.
    Returns data for both stocks and their Pearson correlation coefficient.
    """
    company1 = session.exec(select(Company).where(Company.symbol == symbol1)).first()
    if not company1:
        raise HTTPException(status_code=404, detail=f"Company '{symbol1}' not found")

    company2 = session.exec(select(Company).where(Company.symbol == symbol2)).first()
    if not company2:
        raise HTTPException(status_code=404, detail=f"Company '{symbol2}' not found")

    cutoff_date = date.today() - timedelta(days=days)

    records1 = session.exec(
        select(StockData)
        .where(StockData.company_id == company1.id)
        .where(StockData.date >= cutoff_date)
        .order_by(StockData.date)
    ).all()

    records2 = session.exec(
        select(StockData)
        .where(StockData.company_id == company2.id)
        .where(StockData.date >= cutoff_date)
        .order_by(StockData.date)
    ).all()

    # Compute correlation of daily returns
    returns1 = [r.daily_return for r in records1]
    returns2 = [r.daily_return for r in records2]
    correlation = compute_correlation(returns1, returns2)

    def to_stock_out(r):
        return StockDataOut(
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

    return CompareOut(
        symbol1=company1.symbol,
        symbol1_name=company1.name,
        symbol2=company2.symbol,
        symbol2_name=company2.name,
        symbol1_data=[to_stock_out(r) for r in records1],
        symbol2_data=[to_stock_out(r) for r in records2],
        correlation=correlation,
    )
