from config import get_settings
settings = get_settings()
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

database_url = settings.DATABASE_URL
if not database_url:
    raise ValueError("DATABASE_URL is not set in the environment variables.")

engine=create_engine(database_url)
SessionLocal=sessionmaker(autocommit=False,
                           autoflush=False,
                           bind=engine)