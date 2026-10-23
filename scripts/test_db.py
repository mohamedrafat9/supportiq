import os
import psycopg
from dotenv import load_dotenv

load_dotenv()
database_url=os.getenv("DATABASE_URL")

if not database_url:
    raise ValueError("DATABASE_URL environment variable is not set.")

database_url = database_url.replace(
    "postgresql+psycopg://",
    "postgresql://",
    1,
)

with psycopg.connect(database_url) as conn:
    with conn.cursor() as cur:
        cur.execute("SELECT version();")
        version = cur.fetchone()[0]
        print("Database connection successful!")
        print(version)