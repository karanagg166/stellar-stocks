from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlmodel import Session, select

from app.database import get_session
from app.models import Company, StockData

router = APIRouter()


class MoverItem(BaseModel):
    symbol: str
    name: str
    daily_return: float
    close: float


class TopMoversOut(BaseModel):
    gainers: list[MoverItem]
    losers: list[MoverItem]


@router.get("/top-movers", response_model=TopMoversOut)
def get_top_movers(session: Session = Depends(get_session)):
    """
    Returns the top 5 gainers and top 5 losers by daily return
    based on the most recent trading day's data.
    """
    companies = session.exec(select(Company)).all()

    movers: list[MoverItem] = []

    for company in companies:
        # Get the latest stock data record
        latest = session.exec(
            select(StockData)
            .where(StockData.company_id == company.id)
            .order_by(StockData.date.desc())
        ).first()
        
        if latest:
            movers.append(
                MoverItem(
                    symbol=company.symbol,
                    name=company.name,
                    daily_return=round(latest.daily_return * 100, 2),
                    close=round(latest.close, 2),
                )
            )

    # Sort by daily return
    movers.sort(key=lambda x: x.daily_return, reverse=True)

    return TopMoversOut(
        gainers=movers[:5],
        losers=list(reversed(movers[-5:])),
    )
