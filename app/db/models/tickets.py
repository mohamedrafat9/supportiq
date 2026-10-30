from sqlalchemy import Integer, String, CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column
from .base import Base

class Ticket(Base):
    __tablename__ = "tickets"

    __table_args__=(
        CheckConstraint(
            "status IN ('open','in_progress','resolved','closed')",
            name="check_ticket_status",
        ),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="open")