from sqlalchemy.orm import Session
from sqlalchemy import select

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
    db.commit()
    db.refresh(ticket)

    return ticket

def get_ticket_by_id(db: Session, ticket_id: int) -> Ticket | None:
    statement = select(Ticket).where(Ticket.id == ticket_id)
    return db.scalars(statement).first()

def update_ticket_status(
        db:Session,
        ticket_id:int,
        new_status:str
) -> Ticket |None:
    ticket = get_ticket_by_id(db,ticket_id)

    if ticket is None:
        return None
    ticket.status=new_status
    db.commit()
    db.refresh(ticket)

    return ticket

                              