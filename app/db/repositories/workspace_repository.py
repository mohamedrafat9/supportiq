from uuid import UUID 
from sqlalchemy.orm import Session
from app.db.models.workspaces import Workspace

def get_workspace_by_id(
        db: Session,
        workspace_id: UUID
        ) -> Workspace | None:
    return db.get(Workspace, workspace_id)