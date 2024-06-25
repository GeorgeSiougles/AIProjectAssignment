from sqlalchemy.orm import Session
from app.models import TaxInfo

def test_home(test_client):
    response = test_client.get("/")
    assert response.status_code == 200
    assert "Total Income" in response.text  

def test_submit_tax_info(test_client, test_db):
    response = test_client.post("/submit/", data={
        "income": 5000,
        "expenses": 1500,
        "tax_rate": 24,
        "description": "Test entry"
    })

    assert response.status_code == 200  

    entry = test_db.query(TaxInfo).filter_by(description="Test entry").first()
    assert entry is not None
    assert entry.income == 5000
    assert entry.expenses == 1500
    assert entry.tax_amount == round(1500 * 0.24, 2)

def test_delete_entry(test_client, test_db: Session):
    test_entry = TaxInfo(income=2000, expenses=500, tax_amount=120, tax_rate=24, description="Delete entry")
    test_db.add(test_entry)
    test_db.commit()
    test_db.refresh(test_entry)

    response = test_client.post(f"/delete/{test_entry.id}")
    assert response.status_code == 200  

    entry = test_db.query(TaxInfo).filter_by(id=test_entry.id).first()
    assert entry is None


def test_clear_all_entries(test_client, test_db: Session):
    test_db.add_all([
        TaxInfo(income=1000, expenses=300, tax_amount=72, tax_rate=24, description="Entry 1"),
        TaxInfo(income=1500, expenses=400, tax_amount=96, tax_rate=24, description="Entry 2")
    ])
    test_db.commit()

    response = test_client.post("/clear_all/")
    assert response.status_code == 200  

    entries = test_db.query(TaxInfo).all()
    assert len(entries) == 0

