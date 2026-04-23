from fastapi import APIRouter, Depends
from sqlmodel import Session, select

from app.database import get_session
from app.models import Company
from app.schemas.company import CompanyOut, CompanyListOut

router = APIRouter()


@router.get("/companies", response_model=CompanyListOut)
def get_companies(session: Session = Depends(get_session)):
    """
    Returns a list of all available companies with their symbols,
    names, and sectors.
    """
    companies = session.exec(select(Company).order_by(Company.symbol)).all()

    return CompanyListOut(
        count=len(companies),
        companies=[
            CompanyOut(
                id=c.id,
                symbol=c.symbol,
                name=c.name,
                sector=c.sector,
            )
            for c in companies
        ],
    )
