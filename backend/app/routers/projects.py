from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.core.database import get_db
from app.dependencies.auth import get_current_user
from app.schemas.project import ProjectCreate, ProjectOut
from app.models.project import Project
from app.services.subscription_service import enforce_project_limit
from app.services.audit_service import log_action

router = APIRouter(prefix="/projects", tags=["Projects"])

@router.post("", response_model=ProjectOut)
def create_project(payload: ProjectCreate, db: Session = Depends(get_db), user=Depends(get_current_user)):
    enforce_project_limit(db, user.id)
    project = Project(name=payload.name, description=payload.description, owner_id=user.id)
    db.add(project)
    db.flush()

    log_action(db, user.id, "create", "project", str(project.id), {"name": project.name})
    db.commit()
    db.refresh(project)
    return project

@router.get("", response_model=list[ProjectOut])
def list_projects(db: Session = Depends(get_db), user=Depends(get_current_user)):
    stmt = select(Project).where(Project.owner_id == user.id).order_by(Project.created_at.desc())
    return list(db.scalars(stmt).all())

@router.delete("/{project_id}")
def delete_project(project_id: int, db: Session = Depends(get_db), user=Depends(get_current_user)):
    project = db.get(Project, project_id)
    if not project or project.owner_id != user.id:
        return {"deleted": False}
    db.delete(project)
    log_action(db, user.id, "delete", "project", str(project_id), {})
    db.commit()
    return {"deleted": True}
