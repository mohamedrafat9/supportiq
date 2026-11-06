from datetime import datetime
from uuid import UUID, uuid4
from sqlalchemy import (
    BigInteger,
    CheckConstraint,
    DateTime,
    ForeignKey,
    String,
    Uuid,
    func,
    Text,

)
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import UniqueConstraint
from .base import Base

class Document(Base):
    __tablename__ = "documents"

    __table_args__ = (
        CheckConstraint(
            "status IN ('uploaded', 'processing', 'completed', 'failed')",
            name="check_document_status",
        ),
        UniqueConstraint(
            "workspace_id",
            "content_hash",
            name="uq_document_workspace_content_hash"
        ),
    )

    id: Mapped[UUID]= mapped_column(
        Uuid,
        primary_key=True,
        default=uuid4,
    )
    workspace_id: Mapped[UUID] = mapped_column(
        Uuid,
        ForeignKey("workspaces.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    original_filename: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )
    storage_path: Mapped[str] = mapped_column(
        String(1024),
        nullable=False,
    )

    mime_type: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    file_size_bytes: Mapped[int] = mapped_column(
        BigInteger,
        nullable=False,
    )

    status: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        default="uploaded",
    )

    error_message: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )

    processed_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    workspace: Mapped["Workspace"] = relationship(
        back_populates="documents",
    )

    content_hash: Mapped[str] = mapped_column(
        String(64),
        nullable=False,
    )
