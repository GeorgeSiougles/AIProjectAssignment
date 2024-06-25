import pytest
from fastapi import HTTPException
from .validation import validate_income, validate_expenses

def test_validate_income_positive():
    validate_income(100.0) 

def test_validate_income_negative():
    with pytest.raises(HTTPException):
        validate_income(-100.0)  

def test_validate_expenses_positive():
    validate_expenses(100.0)  
    
def test_validate_expenses_negative():
    with pytest.raises(HTTPException):
        validate_expenses(-100.0)  
