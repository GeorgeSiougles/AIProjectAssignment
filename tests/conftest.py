"""
Test setup module for FastAPI application.

This module sets up the necessary fixtures and configurations for testing the FastAPI application.
It includes creating an in-memory SQLite database, setting up SQLAlchemy session factories, 
and configuring the FastAPI test client.

Fixtures:
    test_db: A pytest fixture that sets up and tears down the test database.
    test_client: A pytest fixture that provides a test client for making requests to the FastAPI application.
"""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app, get_db
from app.database import Base

# SQLAlchemy database URL for testing (using SQLite in-memory database)
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

# Create SQLAlchemy engine for the test database
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})

# Create a sessionmaker factory for the test database
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create all database tables for the test database
Base.metadata.create_all(bind=engine)

@pytest.fixture(scope="module")
def test_db():
    """
    Pytest fixture to set up and tear down the test database.

    This fixture creates a new database session for a test module, drops all tables 
    before starting the tests, and recreates them. The session is closed after 
    the tests are done.

    Yields:
        Session: A SQLAlchemy session connected to the test database.
    """
    # Drop all tables and recreate them before running the tests
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

@pytest.fixture(scope="module")
def test_client():
    """
    Pytest fixture to provide a test client for the FastAPI application.

    This fixture overrides the `get_db` dependency to use the test database session. 
    It then creates a TestClient for making requests to the FastAPI application.

    Yields:
        TestClient: A test client for making requests to the FastAPI application.
    """
    def override_get_db():
        """
        Override function for the `get_db` dependency.

        This function provides a database session connected to the test database.

        Yields:
            Session: A SQLAlchemy session connected to the test database.
        """
        try:
            db = TestingSessionLocal()
            yield db
        finally:
            db.close()

    # Override the get_db dependency in the FastAPI app to use the test database
    app.dependency_overrides[get_db] = override_get_db
    # Create a TestClient for the FastAPI app
    client = TestClient(app)
    yield client
