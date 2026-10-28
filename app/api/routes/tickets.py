
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import SessionLocal
from app.db.repositories.ticket_repository import (
    create_ticket,
    get_ticket_by_id,
)
from app.schemas.ticket import TicketCreate, TicketRead


router = APIRouter(prefix="/tickets", tags=["Tickets"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post(
    "/",
    response_model=TicketRead,
    status_code=status.HTTP_201_CREATED,
)
def create_new_ticket(
    ticket_data: TicketCreate,
    db: Session = Depends(get_db),
    status:str | None = None
):
    return create_ticket(
        db=db,
        title=ticket_data.title,
        status=status
    )


@router.get(
    "/{ticket_id}",
    response_model=TicketRead,
)
def read_ticket(
    ticket_id: int,
    db: Session = Depends(get_db),
):
    ticket = get_ticket_by_id(db=db, ticket_id=ticket_id)

    if ticket is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ticket not found",
        )

    return ticket
