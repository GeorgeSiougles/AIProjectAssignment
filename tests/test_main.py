from sqlalchemy.orm import Session  # Import SQLAlchemy session
from app.models import TaxInfo  # Import the TaxInfo model

def test_home(test_client):
    """
    Test the home route for correct status code and content.

    This test checks if the home route ("/") returns a status code of 200 (OK) 
    and contains the text "Total Income" in the response content.

    Args:
        test_client (TestClient): A test client for making requests to the FastAPI application.
    """
    response = test_client.get("/")  # Send GET request to home route
    assert response.status_code == 200  # Check if the status code is 200
    assert "Total Income" in response.text  # Check if "Total Income" is in the response content

def test_submit_tax_info(test_client, test_db):
    """
    Test submitting new tax information.

    This test sends a POST request to submit new tax information and checks if the entry is 
    correctly created in the database.

    Args:
        test_client (TestClient): A test client for making requests to the FastAPI application.
        test_db (Session): A SQLAlchemy session connected to the test database.
    """
    # Send POST request to submit tax info
    response = test_client.post("/submit/", data={
        "income": 5000,
        "expenses": 1500,
        "tax_rate": 24,
        "description": "Test entry"
    })

    assert response.status_code == 200  # Check if the status code is 200

    # Query the database for the new entry
    entry = test_db.query(TaxInfo).filter_by(description="Test entry").first()
    assert entry is not None  # Check if the entry is not None (exists)
    assert entry.income == 5000  # Check if the income is correct
    assert entry.expenses == 1500  # Check if the expenses are correct
    assert entry.tax_amount == round(1500 * 0.24, 2)  # Check if the tax amount is correct

def test_delete_entry(test_client, test_db: Session):
    """
    Test deleting a specific tax information entry by ID.

    This test creates a test entry, sends a POST request to delete it, and checks if the 
    entry is correctly deleted from the database.

    Args:
        test_client (TestClient): A test client for making requests to the FastAPI application.
        test_db (Session): A SQLAlchemy session connected to the test database.
    """
    # Create a test entry
    test_entry = TaxInfo(income=2000, expenses=500, tax_amount=120, tax_rate=24, description="Delete entry")
    test_db.add(test_entry)
    test_db.commit()
    test_db.refresh(test_entry)

    # Send POST request to delete the entry
    response = test_client.post(f"/delete/{test_entry.id}")
    assert response.status_code == 200  # Check if the status code is 200

    # Query the database to check if the entry is deleted
    entry = test_db.query(TaxInfo).filter_by(id=test_entry.id).first()
    assert entry is None  # Check if the entry is None (deleted)

def test_clear_all_entries(test_client, test_db: Session):
    """
    Test clearing all tax information entries.

    This test creates multiple test entries, sends a POST request to clear all entries, 
    and checks if the database is empty after the operation.

    Args:
        test_client (TestClient): A test client for making requests to the FastAPI application.
        test_db (Session): A SQLAlchemy session connected to the test database.
    """
    # Create multiple test entries
    test_db.add_all([
        TaxInfo(income=1000, expenses=300, tax_amount=72, tax_rate=24, description="Entry 1"),
        TaxInfo(income=1500, expenses=400, tax_amount=96, tax_rate=24, description="Entry 2")
    ])
    test_db.commit()

    # Send POST request to clear all entries
    response = test_client.post("/clear_all/")
    assert response.status_code == 200  # Check if the status code is 200

    # Query the database to check if all entries are deleted
    entries = test_db.query(TaxInfo).all()
    assert len(entries) == 0  # Check if the number of entries is 0 (cleared)
