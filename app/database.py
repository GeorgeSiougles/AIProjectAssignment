"""
Database configuration module.

This module is responsible for setting up the database connection and ORM base class
using SQLAlchemy. It also loads environment variables required for the database 
configuration from a .env.local file.

Attributes:
    BASEDIR (str): The base directory of the current file.
    DATABASE_URL (str): The database URL, retrieved from environment variables or 
                        defaulting to a SQLite database.
    engine (Engine): SQLAlchemy engine created with the specified DATABASE_URL.
    SessionLocal (sessionmaker): A sessionmaker factory bound to the engine, with 
                                 autocommit and autoflush settings.
    Base (DeclarativeMeta): A base class for all ORM models.
"""

import os  # Module for interacting with the operating system
from sqlalchemy import create_engine  # Function to create a SQLAlchemy engine
from sqlalchemy.ext.declarative import declarative_base  # Function to create a base class for ORM models
from sqlalchemy.orm import sessionmaker  # Function to create a sessionmaker factory
from dotenv import load_dotenv  # Function to load environment variables from a .env file

# Define the base directory of the current file
BASEDIR = os.path.abspath(os.path.dirname(__file__))

# Load environment variables from a .env.local file located in the base directory
load_dotenv(os.path.join(BASEDIR, '.env.local'))

# Get the database URL from the environment variables; default to a SQLite database if not set
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./test_db.sqlite")

# Create a SQLAlchemy engine with the specified DATABASE_URL
# For SQLite, the `connect_args` parameter is used to allow multi-threading
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

# Create a sessionmaker factory bound to the engine
# autocommit=False ensures that sessions do not automatically commit after each transaction
# autoflush=False ensures that changes are not automatically flushed to the database
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create a base class for all ORM models using the declarative_base function
Base = declarative_base()
