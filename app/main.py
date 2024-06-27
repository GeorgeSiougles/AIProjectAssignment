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

@app.get("/", response_class=HTMLResponse)
async def home(request: Request, db: Session = Depends(get_db)):
    """
    Home route to display all tax information entries and totals.

    This function handles GET requests to the root URL ("/"). It queries all tax 
    information entries from the database, calculates total income, expenses, and 
    tax amounts, and then renders the "home.html" template with the retrieved data.

    Args:
        request (Request): The request object, which includes all information about the HTTP request.
        db (Session): The database session dependency, provided by FastAPI's Depends function.

    Returns:
        HTMLResponse: The rendered "home.html" template with the following context:
            - request: The original request object.
            - entries: A list of TaxInfoResponse objects representing all tax entries.
            - total_income: The total income calculated from all entries.
            - total_expenses: The total expenses calculated from all entries.
            - total_tax: The total tax amount calculated from all entries.
    """
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

@app.post("/submit/", response_model=TaxInfoResponse)
async def submit_tax_info(
    income: float = Form(...),
    expenses: float = Form(...),
    tax_rate: float = Form(24),
    description: str = Form(None),
    db: Session = Depends(get_db)
):
    """
    Route to submit new tax information entry.

    This function handles POST requests to the "/submit/" URL. It validates the 
    provided income and expenses, calculates the tax amount based on the tax rate, 
    creates a new tax information entry, and saves it to the database. After 
    submission, it redirects to the home page.

    Args:
        income (float): The income amount submitted via the form.
        expenses (float): The expenses amount submitted via the form.
        tax_rate (float): The tax rate to be applied. Default is 24.
        description (str, optional): An optional description for the tax entry.
        db (Session): The database session dependency, provided by FastAPI's Depends function.

    Returns:
        RedirectResponse: Redirects to the home page ("/") with status code 303.
    """
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


@app.post("/delete/{entry_id}", response_class=HTMLResponse)
async def delete_entry(entry_id: int, db: Session = Depends(get_db)):
    """
    Route to delete a specific tax information entry by ID.

    This function handles POST requests to the "/delete/{entry_id}" URL. It queries 
    the database for the tax information entry with the specified ID. If the entry 
    exists, it is deleted from the database. After deletion, the function redirects 
    to the home page.

    Args:
        entry_id (int): The ID of the tax information entry to be deleted.
        db (Session): The database session dependency, provided by FastAPI's Depends function.

    Returns:
        RedirectResponse: Redirects to the home page ("/") with status code 303.
    """
    # Query the entry by ID
    entry = db.query(TaxInfo).filter(TaxInfo.id == entry_id).first()
    
    # If entry exists, delete it from the database
    if entry:
        db.delete(entry)
        db.commit()
    
    # Redirect to home page after deletion
    return RedirectResponse(url="/", status_code=303)


@app.post("/clear_all/", response_class=HTMLResponse)
async def clear_all_entries(db: Session = Depends(get_db)):
    """
    Route to clear all tax information entries.

    This function handles POST requests to the "/clear_all/" URL. It deletes all 
    tax information entries from the database and then redirects to the home page.

    Args:
        db (Session): The database session dependency, provided by FastAPI's Depends function.

    Returns:
        RedirectResponse: Redirects to the home page ("/") with status code 303.
    """
    # Delete all entries from the database
    db.query(TaxInfo).delete()
    db.commit()
    
    # Redirect to home page after clearing entries
    return RedirectResponse(url="/", status_code=303)

@app.get("/get_all_advice/", response_class=HTMLResponse)
async def get_all_advice(request: Request, db: Session = Depends(get_db)):
    """
    Route to get tax advice based on all tax information entries.

    This function handles GET requests to the "/get_all_advice/" URL. It queries all 
    tax information entries from the database and uses OpenAI's GPT-3.5-turbo model 
    to provide tax advice based on the retrieved data. The advice is then rendered 
    on the "advice.html" template.

    Args:
        request (Request): The request object, which includes all information about the HTTP request.
        db (Session): The database session dependency, provided by FastAPI's Depends function.

    Returns:
        HTMLResponse: The rendered "advice.html" template with the following context:
            - request: The original request object.
            - advice_list: A list of tax advice strings. If no entries are found, a message indicating no entries are available is returned.
    """
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

