from fastapi import HTTPException


def validate_positive_number(value: float, field_name: str):
    """
    Check if a given number is positive and raise an exception if it is a negative number

    Parameters:
        value (float): The value to be checked
        field_name (str): The name of the value that is checked
    """
    if value < 0:
        raise HTTPException(status_code=400, detail=f"{field_name} must be a positive number")


def validate_income(income: float):
    '''
    Invoke positive validate_positive_number() with the proper field name to raise an exception 

    Parameters:
        income (float): the amount of income
    
    '''
    validate_positive_number(income, "Income")


def validate_expenses(expenses: float):
    '''
    Invoke positive validate_positive_number() with the proper field name to raise an exception 

    Parameters:
        expenses (float): the amount of expenses
    
    '''
    validate_positive_number(expenses, "Expenses")
