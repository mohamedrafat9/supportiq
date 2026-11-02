import pytest

from sqlalchemy.orm import Session
from fastapi.testclient import TestClient

from app.main import app
from app.db.dependencies import get_db
from app.db.models import Base
from tests.test_database import test_engine


@pytest.fixture(scope="session", autouse=True)
def setup_test_database():
    Base.metadata.create_all(bind=test_engine)
    yield


@pytest.fixture
def db_session(setup_test_database):
    connection = test_engine.connect()
    transaction = connection.begin()

    db = Session(
        bind=connection,
        join_transaction_mode="create_savepoint",
    )

    try:
        yield db
    finally:
        db.close()
        transaction.rollback()
        connection.close()


@pytest.fixture
def client(db_session):
    def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.pop(get_db, None)