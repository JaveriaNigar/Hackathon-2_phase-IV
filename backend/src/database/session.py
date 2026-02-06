from sqlmodel import create_engine, Session
from typing import Generator
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get database URL from environment variable
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    # Fallback to root directory .env file
    load_dotenv(dotenv_path="../../.env.local")
    DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    # Fallback to root directory .env file (alternative path)
    load_dotenv(dotenv_path="../.env.local")
    DATABASE_URL = os.getenv("DATABASE_URL")

# If using SQLite and the path is relative, convert it to absolute
if DATABASE_URL and DATABASE_URL.startswith("sqlite:///"):
    # Extract the path part (everything after sqlite:///)
    path_part = DATABASE_URL[10:]  # Remove "sqlite:///"

    # If it's a relative path (starts with ./ or ../), convert to absolute
    if path_part.startswith("./") or path_part.startswith("../"):
        # Get the absolute path relative to the project root (two levels up from src/database)
        abs_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", path_part))
        DATABASE_URL = f"sqlite:///{abs_path}"
        print(f"Converted relative DB path to absolute: {DATABASE_URL}")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL environment variable is not set. Please check your .env file.")

# Create the database engine
engine = create_engine(DATABASE_URL, echo=True)

def get_session() -> Generator[Session, None, None]:
    with Session(engine) as session:
        try:
            yield session
            session.commit()  # Commit the transaction
        except Exception:
            session.rollback()  # Rollback in case of error
            raise