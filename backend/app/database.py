from sqlmodel import create_engine, SQLModel, Session
from app.config import settings

engine = create_engine(settings.DATABASE_URL, echo=False)


def create_db_and_tables():
    """Create all database tables based on SQLModel definitions."""
    # Import models here to ensure they are registered with SQLModel
    from app.models import Company, StockData  # noqa: F401
    SQLModel.metadata.create_all(engine)


def get_session():
    """Dependency for getting a database session."""
    with Session(engine) as session:
        yield session
