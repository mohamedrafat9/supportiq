from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.dependencies import get_db
from app.db.repositories.ticket_repository import (
    get_all_tickets,
    get_ticket_by_id,
)
from app.schemas.ticket import TicketCreate, TicketRead, TicketUpdate
from app.services.ticket_service import (
    create_ticket_service,
    update_ticket_status_service,
    delete_ticket_service,
)

router = APIRouter(
    prefix="/tickets",
    tags=["Tickets"],
)


@router.post(
    "/",
    response_model=TicketRead,
    status_code=status.HTTP_201_CREATED,
)
def create_new_ticket(
    ticket_data: TicketCreate,
    db: Session = Depends(get_db),
):
    return create_ticket_service(
        db=db,
        title=ticket_data.title,
    )


@router.get(
    "/",
    response_model=list[TicketRead],
)
def get_tickets(
    db: Session = Depends(get_db),
):
    return get_all_tickets(db=db)


@router.get(
    "/{ticket_id}",
    response_model=TicketRead,
)
def get_ticket(
    ticket_id: int,
    db: Session = Depends(get_db),
):
    ticket = get_ticket_by_id(
        db=db,
        ticket_id=ticket_id,
    )

    if ticket is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ticket not found",
        )

    return ticket


@router.put(
    "/{ticket_id}",
    response_model=TicketRead,
)
def update_ticket(
    ticket_id: int,
    ticket_data: TicketUpdate,
    db: Session = Depends(get_db),
):
    try:
        ticket = update_ticket_status_service(
            db=db,
            ticket_id=ticket_id,
            new_status=ticket_data.status,
        )

    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(error),
        )

    if ticket is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ticket not found",
        )

    return ticket


@router.delete(
    "/{ticket_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_ticket(
    ticket_id: int,
    db: Session = Depends(get_db),
):
    deleted = delete_ticket_service(
        db=db,
        ticket_id=ticket_id,
    )

    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="the ticket wasn't found",
        )

    return None