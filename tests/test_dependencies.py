import pytest
from unittest.mock import MagicMock

from app.db.dependencies import get_db


def test_get_db(monkeypatch):
    mock_session = MagicMock()

    monkeypatch.setattr(
        "app.db.dependencies.SessionLocal",
        lambda: mock_session
    )

    db_generator = get_db()

    yielded_session = next(db_generator)

    assert yielded_session is mock_session

    db_generator.close()

    mock_session.close.assert_called_once()