from fastapi.testclient import TestClient
from app.models import TaxInfo


def test_create_entry(test_client: TestClient):
    response = test_client.post("/submit/", data={
        "income": 5000,
        "expenses": 1500,
        "tax_rate": 24,
        "description": "Test entry"
    })
    assert response.status_code == 303  # Redirect response

    with test_client.app.dependency_overrides.get_db() as db:
        entry = db.query(TaxInfo).filter(TaxInfo.income == 5000).first()
        assert entry is not None
        assert entry.expenses == 1500
        assert entry.tax_rate == 24
        assert entry.description == "Test entry"


def test_delete_entry(test_client: TestClient):
    with test_client.app.dependency_overrides.get_db() as db:
        new_entry = TaxInfo(
            income=4000, expenses=1000, tax_rate=24, description="Entry to delete"
        )
        db.add(new_entry)
        db.commit()
        db.refresh(new_entry)

        entry_id = new_entry.id

    response = test_client.post(f"/delete/{entry_id}")
    assert response.status_code == 303  # Redirect response

    with test_client.app.dependency_overrides.get_db() as db:
        entry = db.query(TaxInfo).filter(TaxInfo.id == entry_id).first()
        assert entry is None


def test_clear_all_entries(test_client: TestClient):
    with test_client.app.dependency_overrides.get_db() as db:
        entries = [
            TaxInfo(income=2000, expenses=500, tax_rate=24, description="Entry 1"),
            TaxInfo(income=3000, expenses=800, tax_rate=24, description="Entry 2")
        ]
        db.add_all(entries)
        db.commit()

    response = test_client.post("/clear_all/")
    assert response.status_code == 303  # Redirect response

    with test_client.app.dependency_overrides.get_db() as db:
        entries = db.query(TaxInfo).all()
        assert len(entries) == 0
