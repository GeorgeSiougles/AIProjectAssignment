from pydantic import BaseModel
from sqlalchemy import Column, Integer, Float, String
from .database import Base


class TaxInfo(Base):
    __tablename__ = "tax_info"

    id = Column(Integer, primary_key=True, index=True)
    income = Column(Float, nullable=False)
    expenses = Column(Float, nullable=False)
    tax_amount = Column(Float, nullable=False)
    tax_rate = Column(Float, nullable=False)
    description = Column(String, nullable=True)


class TaxInfoResponse(BaseModel):
    id: int
    income: float
    expenses: float
    tax_amount: float
    tax_rate: float
    description: str | None = None

    class Config:
        orm_mode = True
        from_attributes = True
