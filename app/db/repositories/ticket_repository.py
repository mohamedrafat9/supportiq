from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.models.tickets import Ticket


def create_ticket(
    db: Session,
    title: str,
    status: str = "open",
) -> Ticket:
    ticket = Ticket(
        title=title,
        status=status,
    )

    db.add(ticket)
    db.flush()

    return ticket


def get_ticket_by_id(
    db: Session,
    ticket_id: int,
) -> Ticket | None:
    return db.get(Ticket, ticket_id)


def get_all_tickets(
    db: Session,
) -> list[Ticket]:
    statement = select(Ticket)
    return db.scalars(statement).all()


def delete_ticket_by_id(
    db: Session,
    ticket_id: int,
) -> bool:
    ticket = get_ticket_by_id(db, ticket_id)

    if ticket is None:
        return False

    db.delete(ticket)
    db.flush()

    return True


def update_ticket_status(
    db: Session,
    ticket: Ticket,
    new_status: str,
) -> Ticket:
    ticket.status = new_status

    db.flush()

    return ticket