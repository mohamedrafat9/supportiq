from fastapi import APIRouter, Depends, HTTPException as httpex, status
from sqlalchemy.orm import Session

from app.db.dependencies import get_db

from app.db.repositories.ticket_repository import*

from app.schemas.ticket import*

router = APIRouter(prefix="/tickets", tags=["Tickets"])



@router.post(
    "/",
    response_model=TicketRead,
    status_code=status.HTTP_201_CREATED,
)
def create_new_ticket(
    ticket_data: TicketCreate,
    db: Session = Depends(get_db),
):
    return create_ticket(
        db=db,
        title=ticket_data.title,
    )


@router.get(
    "/",
    response_model=list[TicketRead],
)
def read_all_tickets(
    db: Session = Depends(get_db),
):
    return get_all_tickets(db=db)


@router.get(
    "/{ticket_id}",
    response_model=TicketRead,
    status_code=status.HTTP_200_OK
)
def read_ticket(
    ticket_id: int,
    db: Session = Depends(get_db),
):
    ticket = get_ticket_by_id(db=db, ticket_id=ticket_id)

    if ticket is None:
        raise httpex(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ticket not found",
        )

    return ticket


@router.put(
    "/{ticket_id}",
    response_model=TicketRead,
    status_code=status.HTTP_200_OK
)
def update_ticket( 
    ticket_id: int,
    ticket_data:TicketUpdate,
    db: Session = Depends(get_db),
):
    updated_ticket = update_ticket_status(
        db=db,
        ticket_id=ticket_id,
        new_status=ticket_data.status,
    )
    if updated_ticket is None:
        raise httpex(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ticket not found",
        )


    return updated_ticket


@router.delete(
    "/{ticket_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
def delete_ticket(
    ticket_id:int,
    db:Session=Depends(get_db)
):
    deletion=delete_ticket_by_id(db=db,ticket_id=ticket_id)
    if deletion is False:
        raise httpex(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="the ticket wasn't found"
        )
    return None 
