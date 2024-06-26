import os
from dotenv import load_dotenv
import openai
from fastapi import FastAPI, Request, Form, Depends, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from .models import TaxInfo, TaxInfoResponse
from .database import SessionLocal, engine, Base
from .validation import validate_expenses, validate_income

# Set the base directory and load environment variables
BASEDIR = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(BASEDIR, '.env.local'))

# Set OpenAI API key from environment variable
openai.api_key = os.getenv("OPENAI-API-KEY")

# Create all database tables
Base.metadata.create_all(bind=engine)

# Initialize FastAPI app and Jinja2 templates
app = FastAPI()
templates = Jinja2Templates(directory="app/templates")

# Dependency to get database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Home route to display all tax information entries and totals
@app.get("/", response_class=HTMLResponse)
async def home(request: Request, db: Session = Depends(get_db)):
    # Query all tax info entries from the database
    taxinfo_entries = db.query(TaxInfo).all()
    entries = [TaxInfoResponse.from_orm(entry) for entry in taxinfo_entries]
    # Calculate total income, expenses, and tax
    total_income = round(sum(entry.income for entry in entries), 2)
    total_expenses = round(sum(entry.expenses for entry in entries), 2)
    total_tax = round(sum(entry.tax_amount for entry in entries), 2)
    # Render home template with the entries and totals
    return templates.TemplateResponse("home.html", {
        "request": request,
        "entries": entries,
        "total_income": total_income,
        "total_expenses": total_expenses,
        "total_tax": total_tax
    })

# Route to submit new tax information entry
@app.post("/submit/", response_model=TaxInfoResponse)
async def submit_tax_info(
    income: float = Form(...),
    expenses: float = Form(...),
    tax_rate: float = Form(24),
    description: str = Form(None),
    db: Session = Depends(get_db)
):
    # Validate income and expenses
    validate_income(income)
    validate_expenses(expenses)

    # Calculate tax amount
    tax_amount = round(expenses * (tax_rate / 100), 2)
    # Create new TaxInfo entry
    db_tax_info = TaxInfo(
        income=round(income, 2),
        expenses=round(expenses, 2),
        tax_amount=tax_amount,
        tax_rate=tax_rate,
        description=description
    )
    # Add and commit the new entry to the database
    db.add(db_tax_info)
    db.commit()
    db.refresh(db_tax_info)
    # Redirect to home page after submission
    return RedirectResponse(url="/", status_code=303)

# Route to delete a specific tax information entry by ID
@app.post("/delete/{entry_id}", response_class=HTMLResponse)
async def delete_entry(entry_id: int, db: Session = Depends(get_db)):
    # Query the entry by ID
    entry = db.query(TaxInfo).filter(TaxInfo.id == entry_id).first()
    # If entry exists, delete it from the database
    if entry:
        db.delete(entry)
        db.commit()
    # Redirect to home page after deletion
    return RedirectResponse(url="/", status_code=303)

# Route to clear all tax information entries
@app.post("/clear_all/", response_class=HTMLResponse)
async def clear_all_entries(db: Session = Depends(get_db)):
    # Delete all entries from the database
    db.query(TaxInfo).delete()
    db.commit()
    # Redirect to home page after clearing entries
    return RedirectResponse(url="/", status_code=303)

# Route to get tax advice based on all tax information entries
@app.get("/get_all_advice/", response_class=HTMLResponse)
async def get_all_advice(request: Request, db: Session = Depends(get_db)):
    # Query all tax info entries from the database
    taxinfo_entries = db.query(TaxInfo).all()
    entries = [TaxInfoResponse.from_orm(entry) for entry in taxinfo_entries]

    # If no entries found, return with a message
    if not entries:
        return templates.TemplateResponse("advice.html", {"request": request, "advice_list": ["No tax information entries found."]})

    # Prepare the prompt for OpenAI API
    prompt_entries = "\n".join([
        f"Entry {entry.id}: Income = {entry.income}, Expenses = {entry.expenses}, Tax Rate = {entry.tax_rate}%"
        for entry in entries
    ])
    prompt = f"Based on the following tax information entries, provide tax advice: {prompt_entries}"

    try:
        # Get advice from OpenAI's GPT-3.5-turbo model
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a tax advisor."},
                {"role": "user", "content": prompt}
            ]
        )
        advice = response.choices[0].message['content'].strip()
        # Split the advice into a list of sentences or bullet points
        advice_list = advice.split('\n')
    except Exception as e:
        # Raise an HTTP exception if an error occurs
        raise HTTPException(status_code=500, detail=str(e))

    # Render advice template with the advice list
    return templates.TemplateResponse("advice.html", {"request": request, "advice_list": advice_list})
