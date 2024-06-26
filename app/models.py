from pydantic import BaseModel
from sqlalchemy import Column, Integer, Float, String
from .database import Base


class TaxInfo(Base):
    __tablename__ = "tax_info"  # Name of the table in the database

    id = Column(Integer, primary_key=True, index=True)  # Primary key column
    income = Column(Float, nullable=False)  # Column for income, cannot be null
    expenses = Column(Float, nullable=False)  # Column for expenses, cannot be null
    tax_amount = Column(Float, nullable=False)  # Column for tax amount, cannot be null
    tax_rate = Column(Float, nullable=False)  # Column for tax rate, cannot be null
    description = Column(String, nullable=True)  # Optional column for description


# The Config class inside the TaxInfoResponse model includes configuration settings for Pydantic
class TaxInfoResponse(BaseModel):
    id: int  # ID of the tax info entry
    income: float  # Income amount
    expenses: float  # Expenses amount
    tax_amount: float  # Tax amount
    tax_rate: float  # Tax rate
    description: str | None = None  # Optional description

    class Config:
        orm_mode = True  # Enable ORM mode to work with SQLAlchemy models
        from_attributes = True  # Include attributes from the SQLAlchemy model
