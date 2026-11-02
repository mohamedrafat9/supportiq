from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, inspect
from config import get_settings
from app.db.models import Base

settings = get_settings()

test_engine = create_engine(settings.TEST_DATABASE_URL)

TestingSessionLocal = sessionmaker(
    bind=test_engine,
    autoflush=False,
    autocommit=False,
)


def create_test_tables():
    Base.metadata.create_all(bind=test_engine)


if __name__ == "__main__":
    create_test_tables()
    print("Test database tables created successfully!")
    inspector = inspect(test_engine)
    print(inspector.get_table_names())