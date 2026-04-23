from fastapi import APIRouter, HTTPException, Depends
from sqlmodel import Session, select

from app.database import get_session
from app.models import Company, StockData
from app.schemas.summary import SummaryOut

router = APIRouter()


@router.get("/summary/{symbol}", response_model=SummaryOut)
def get_summary(symbol: str, session: Session = Depends(get_session)):
    """
    Returns 52-week high, low, average close, current price,
    volatility score, and average volume for a given stock.
    """
    company = session.exec(select(Company).where(Company.symbol == symbol)).first()
    if not company:
        raise HTTPException(status_code=404, detail=f"Company '{symbol}' not found")

    # Get all stock data for this company
    records = session.exec(
        select(StockData)
        .where(StockData.company_id == company.id)
        .order_by(StockData.date)
    ).all()

    if not records:
        raise HTTPException(
            status_code=404, detail=f"No stock data found for '{symbol}'"
        )

    latest = records[-1]
    closes = [r.close for r in records]
    volumes = [r.volume for r in records]

    # Calculate 1-year total return
    first_close = records[0].close
    last_close = latest.close
    total_return = round(((last_close - first_close) / first_close) * 100, 2)

    return SummaryOut(
        symbol=company.symbol,
        name=company.name,
        sector=company.sector,
        current_price=round(latest.close, 2),
        high_52w=round(latest.high_52w, 2),
        low_52w=round(latest.low_52w, 2),
        avg_close=round(sum(closes) / len(closes), 2),
        total_return_1y=total_return,
        volatility_score=latest.volatility_score,
        volume_avg=round(sum(volumes) / len(volumes), 2),
    )
