import pytest

from app.db.repositories.ticket_repository import create_ticket
from app.services.ticket_service import update_ticket_status_service


def test_cannot_reopen_closed_ticket(db_session):
    ticket = create_ticket(
        db=db_session,
        title="Closed ticket",
        status="closed",
    )

    with pytest.raises(
        ValueError,
        match="Cannot reopen a closed ticket",
    ):
        update_ticket_status_service(
            db=db_session,
            ticket_id=ticket.id,
            new_status="in_progress",
        )

    assert ticket.status == "closed"

def test_update_ticket_status_successfully(db_session):
    ticket = create_ticket(
        db=db_session,
        title="Test ticket",
        status="open",
    )

    updated_ticket = update_ticket_status_service(
        db=db_session,
        ticket_id=ticket.id,
        new_status="in_progress",
    )

    assert updated_ticket is not None
    assert updated_ticket.status == "in_progress"
    assert updated_ticket.id == ticket.id

def test_update_nonexistent_ticket(db_session):
    result = update_ticket_status_service(
        db=db_session,
        ticket_id=99999,
        new_status="in_progress",
    )

    assert result is None