import pytest  # Import pytest for testing
from fastapi import HTTPException  # Import HTTPException for exception handling
from app.validation import validate_income, validate_expenses  # Import validation functions

def test_validate_income_positive():
    """
    Test validate_income function with a positive income value.

    This test ensures that the validate_income function does not raise an exception
    when provided with a valid positive income value.
    """
    validate_income(100.0)  # Validate positive income

def test_validate_income_negative():
    """
    Test validate_income function with a negative income value.

    This test ensures that the validate_income function raises an HTTPException
    when provided with an invalid negative income value.
    """
    with pytest.raises(HTTPException):  # Check if HTTPException is raised
        validate_income(-100.0)  # Validate negative income

def test_validate_expenses_positive():
    """
    Test validate_expenses function with a positive expenses value.

    This test ensures that the validate_expenses function does not raise an exception
    when provided with a valid positive expenses value.
    """
    validate_expenses(100.0)  # Validate positive expenses

def test_validate_expenses_negative():
    """
    Test validate_expenses function with a negative expenses value.

    This test ensures that the validate_expenses function raises an HTTPException
    when provided with an invalid negative expenses value.
    """
    with pytest.raises(HTTPException):  # Check if HTTPException is raised
        validate_expenses(-100.0)  # Validate negative expenses
