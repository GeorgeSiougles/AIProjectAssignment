from fastapi import HTTPException


def validate_positive_number(value: float, field_name: str):
    if value < 0:
        raise HTTPException(status_code=400, detail=f"{field_name} must be a positive number")



def validate_income(income: float):
    validate_positive_number(income, "Income")


def validate_expenses(expenses: float):
    validate_positive_number(expenses, "Expenses")
