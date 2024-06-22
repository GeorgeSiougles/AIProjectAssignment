from fastapi import FastAPI, Request, Form, Depends, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List

from .models import TaxInfo
from .database import SessionLocal, engine, Base
from .validation import validate_expenses, validate_income

Base.metadata.create_all(bind=engine)

app = FastAPI()
templates = Jinja2Templates(directory="app/templates")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class TaxInfoCreate(BaseModel):
    income: float
    expenses: float
    tax_rate: float = 24
    description: str | None = None


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


@app.get("/", response_class=HTMLResponse)
async def home(request: Request, db: Session = Depends(get_db)):
    taxinfo_entries = db.query(TaxInfo).all()
    entries = [TaxInfoResponse.from_orm(entry) for entry in taxinfo_entries]
    total_income = round(sum(entry.income for entry in entries), 2)
    total_expenses = round(sum(entry.expenses for entry in entries), 2)
    total_tax = round(sum(entry.tax_amount for entry in entries), 2)
    return templates.TemplateResponse("home.html", {
        "request": request,
        "entries": entries,
        "total_income": total_income,
        "total_expenses": total_expenses,
        "total_tax": total_tax
    })


@app.post("/submit/", response_model=TaxInfoResponse)
async def submit_tax_info(
    income: float = Form(...),
    expenses: float = Form(...),
    tax_rate: float = Form(24),
    description: str = Form(None),  # Include description field
    db: Session = Depends(get_db)
):
    validate_income(income)
    validate_expenses(expenses)

    tax_amount = round(expenses * (tax_rate / 100), 2)
    db_tax_info = TaxInfo(
        income=round(income, 2),
        expenses=round(expenses, 2),
        tax_amount=tax_amount,
        tax_rate=tax_rate,
        description=description  # Save description
    )
    db.add(db_tax_info)
    db.commit()
    db.refresh(db_tax_info)
    return RedirectResponse(url="/", status_code=303)


@app.post("/delete/{entry_id}", response_class=HTMLResponse)
async def delete_entry(entry_id: int, db: Session = Depends(get_db)):
    entry = db.query(TaxInfo).filter(
        TaxInfo.id == entry_id).first()
    if entry:
        db.delete(entry)
        db.commit()
    return RedirectResponse(url="/", status_code=303)


@app.post("/clear_all/", response_class=HTMLResponse)
async def clear_all_entries(db: Session = Depends(get_db)):
    db.query(TaxInfo).delete()
    db.commit()
    return RedirectResponse(url="/", status_code=303)
