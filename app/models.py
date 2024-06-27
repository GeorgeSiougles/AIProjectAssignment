from pydantic import BaseModel
from sqlalchemy import Column, Integer, Float, String
from .database import Base

class TaxInfo(Base):
    """
    SQLAlchemy model for tax information.

    This class represents the tax information table in the database. It includes 
    columns for income, expenses, tax amount, tax rate, and an optional description.

    Attributes:
        id (int): Primary key column.
        income (float): Income amount, cannot be null.
        expenses (float): Expenses amount, cannot be null.
        tax_amount (float): Tax amount, cannot be null.
        tax_rate (float): Tax rate, cannot be null.
        description (str, optional): Optional description of the tax info.
    """
    __tablename__ = "tax_info"  # Name of the table in the database

    id = Column(Integer, primary_key=True, index=True)  # Primary key column
    income = Column(Float, nullable=False)  # Column for income, cannot be null
    expenses = Column(Float, nullable=False)  # Column for expenses, cannot be null
    tax_amount = Column(Float, nullable=False)  # Column for tax amount, cannot be null
    tax_rate = Column(Float, nullable=False)  # Column for tax rate, cannot be null
    description = Column(String, nullable=True)  # Optional column for description


class TaxInfoResponse(BaseModel):
    """
    Pydantic model for tax information response.

    This class is used to serialize tax information for API responses. It includes 
    fields for income, expenses, tax amount, tax rate, and an optional description.

    Attributes:
        id (int): ID of the tax info entry.
        income (float): Income amount.
        expenses (float): Expenses amount.
        tax_amount (float): Tax amount.
        tax_rate (float): Tax rate.
        description (str, optional): Optional description of the tax info.

    Config:
        orm_mode (bool): Enable ORM mode to work with SQLAlchemy models.
        from_attributes (bool): Include attributes from the SQLAlchemy model.
    """
    id: int  # ID of the tax info entry
    income: float  # Income amount
    expenses: float  # Expenses amount
    tax_amount: float  # Tax amount
    tax_rate: float  # Tax rate
    description: str | None = None  # Optional description

    class Config:
        """
        Pydantic configuration settings.

        Attributes:
            orm_mode (bool): Enable ORM mode to work with SQLAlchemy models.
            from_attributes (bool): Include attributes from the SQLAlchemy model.
        """
        orm_mode = True  # Enable ORM mode to work with SQLAlchemy models
        from_attributes = True  # Include attributes from the SQLAlchemy model

