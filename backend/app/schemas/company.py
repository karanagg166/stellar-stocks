from pydantic import BaseModel


class CompanyOut(BaseModel):
    """Response schema for a single company."""

    id: int
    symbol: str
    name: str
    sector: str

    model_config = {"from_attributes": True}


class CompanyListOut(BaseModel):
    """Response schema for the companies list endpoint."""

    count: int
    companies: list[CompanyOut]
