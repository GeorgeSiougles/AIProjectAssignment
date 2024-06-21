from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from typing import List

app = FastAPI()
templates = Jinja2Templates(directory="app/templates")


class TaxInfo(BaseModel):
    id: int
    income: float
    expenses: float
    tax_amount: float

    def __init__(self, **data):
        super().__init__(**data)
        self.income = round(self.income, 2)
        self.expenses = round(self.expenses, 2)
        self.tax_amount = round(self.tax_amount, 2)


entries: List[TaxInfo] = []
current_id = 1


@app.get("/", response_class=HTMLResponse)
async def get_home(request: Request):
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


@app.post("/submit/")
async def submit_tax_info(request: Request, income: float = Form(...), expenses: float = Form(...), tax_rate: float = Form(24)):
    global current_id
    tax_amount = expenses * (tax_rate / 100)
    tax_info = TaxInfo(id=current_id, income=income,
                       expenses=expenses, tax_amount=tax_amount)
    entries.append(tax_info)
    current_id += 1
    return RedirectResponse(url="/", status_code=303)
