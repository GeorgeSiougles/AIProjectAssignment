from sqlalchemy import Column, Integer, Float

from .database import Base


class TaxInfo(Base):
    __tablename__ = "taxinfo"

    id = Column(Integer, primary_key=True, index=True)
    income = Column(Float, nullable=False)
    expenses = Column(Float, nullable=False)
    tax_amount = Column(Float, nullable=False)
    tax_rate = Column(Float, nullable=False)
