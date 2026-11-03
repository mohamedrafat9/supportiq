from sqlalchemy.orm import Session

from app.db.models.tickets import Ticket
from app.db.repositories.ticket_repository import (
    create_ticket,
    delete_ticket_by_id,
    get_ticket_by_id,
    save_ticket_status,
)


def create_ticket_service(
    db: Session,
    title: str,
) -> Ticket:
    try:
        ticket = create_ticket(
            db=db,
            title=title,
        )

        db.commit()
        db.refresh(ticket)

        return ticket

    except Exception:
        db.rollback()
        raise


def update_ticket_status_service(
    db: Session,
    ticket_id: int,
    new_status: str,
) -> Ticket | None:
    ticket = get_ticket_by_id(
        db=db,
        ticket_id=ticket_id,
    )

    if ticket is None:
        return None

    # Business Rule
    if ticket.status == "closed" and new_status == "in_progress":
        raise ValueError("Cannot reopen a closed ticket")

    try:
        updated_ticket = save_ticket_status(
            db=db,
            ticket=ticket,
            new_status=new_status,
        )

        db.commit()
        db.refresh(updated_ticket)

        return updated_ticket

    except Exception:
        db.rollback()
        raise


def delete_ticket_service(
    db: Session,
    ticket_id: int,
) -> bool:
    try:
        deleted = delete_ticket_by_id(
            db=db,
            ticket_id=ticket_id,
        )

        if not deleted:
            return False

        db.commit()

        return True

    except Exception:
        db.rollback()
        raise