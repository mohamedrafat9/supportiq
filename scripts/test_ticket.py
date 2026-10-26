from app.db.session import SessionLocal
from app.db.repositories.ticket_repository import get_ticket_by_id , update_ticket_status


with SessionLocal() as db:
    ticket = update_ticket_status(
        db=db, 
        ticket_id=1, 
        new_status="in_progress"
        )

    if ticket is None:
        print("Ticket not found")
    else:
        print("Ticket updated successfully!")
        print(f"ID: {ticket.id}")
        print(f"Title: {ticket.title}")
        print(f"Status: {ticket.status}")

