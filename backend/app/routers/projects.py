from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import false
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.dependencies.auth import get_current_user
from app.dependencies.roles import can_access_team_project, require_end_user
from app.models.project import Project
from app.models.team import Team
from app.models.team_member import TeamMember
from app.schemas.project import (ProjectActivityOut, ProjectCreate, ProjectOut,
                                 ProjectUpdate)
from app.services.activity_service import log_project_activity
from app.services.audit_service import log_action
from app.services.cache_service import (get_cached, invalidate_prefix,
                                        set_cached)
from app.services.notification_service import create_notification
from app.services.subscription_service import enforce_project_limit

router = APIRouter(prefix="/projects", tags=["Projects"])


def _notify_team_members(
    db: Session,
    project: Project,
    actor_user_id: int,
    title: str,
    message: str,
    notif_type: str = "info",
):
    if not project.team_id:
        return
    members = db.query(TeamMember).filter(TeamMember.team_id == project.team_id).all()
    for member in members:
        if member.user_id != actor_user_id:
            create_notification(db, member.user_id, title, message, notif_type)


@router.post("", response_model=ProjectOut)
def create_project(
    payload: ProjectCreate,
    db: Session = Depends(get_db),
    user=Depends(require_end_user),
):
    enforce_project_limit(db, user.id)

    project = Project(
        name=payload.name,
        description=payload.description,
        owner_id=user.id,
        team_id=None,
    )
    db.add(project)
    db.flush()

    log_action(
        db, user.id, "create", "project", str(project.id), {"name": project.name}
    )
    log_project_activity(
        db, project.id, user.id, "created", f"Project '{project.name}' created"
    )

    create_notification(
        db,
        user.id,
        "Project created",
        f"Your project '{project.name}' was created successfully.",
        "info",
    )

    db.commit()
    db.refresh(project)
    invalidate_prefix(f"projects:{user.id}:")
    return project


@router.get("", response_model=list[ProjectOut])
def list_projects(
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
):
    cache_key = f"projects:{user.id}:{page}:{page_size}"
    cached = get_cached(cache_key)
    if cached is not None:
        return cached

    offset = (page - 1) * page_size
    team_ids = [
        row[0]
        for row in db.query(TeamMember.team_id)
        .filter(TeamMember.user_id == user.id)
        .all()
    ]
    team_filter = Project.team_id.in_(team_ids) if team_ids else false()
    rows = (
        db.query(Project)
        .filter((Project.owner_id == user.id) | team_filter)
        .order_by(Project.created_at.desc())
        .offset(offset)
        .limit(page_size)
        .all()
    )
    return set_cached(cache_key, rows)


@router.get("/{project_id}", response_model=ProjectOut)
def get_project(
    project_id: int, db: Session = Depends(get_db), user=Depends(get_current_user)
):
    project = db.get(Project, project_id)
    if not project or not can_access_team_project(project, user, db):
        raise HTTPException(status_code=404, detail="Project not found")
    return project


@router.put("/{project_id}", response_model=ProjectOut)
def update_project(
    project_id: int,
    payload: ProjectUpdate,
    db: Session = Depends(get_db),
    user=Depends(require_end_user),
):
    project = db.get(Project, project_id)
    if not project or project.owner_id != user.id:
        raise HTTPException(status_code=404, detail="Project not found")

    if payload.team_id is not None:
        team = db.get(Team, payload.team_id) if payload.team_id else None
        if payload.team_id and (not team or team.owner_id != user.id):
            raise HTTPException(
                status_code=403,
                detail="Only your own teams can be attached to projects",
            )
        project.team_id = payload.team_id

    if payload.name is not None:
        project.name = payload.name
    if payload.description is not None:
        project.description = payload.description

    log_action(db, user.id, "update", "project", str(project.id), {})
    log_project_activity(
        db, project.id, user.id, "updated", f"Project '{project.name}' updated"
    )
    _notify_team_members(
        db,
        project,
        user.id,
        "Project updated",
        f"The team project '{project.name}' was updated.",
    )
    db.commit()
    db.refresh(project)
    invalidate_prefix(f"projects:{user.id}:")
    return project


@router.get("/{project_id}/activity", response_model=list[ProjectActivityOut])
def project_activity(
    project_id: int, db: Session = Depends(get_db), user=Depends(get_current_user)
):
    project = db.get(Project, project_id)
    if not project or not can_access_team_project(project, user, db):
        raise HTTPException(status_code=404, detail="Project not found")
    return project.activities


@router.delete("/{project_id}")
def delete_project(
    project_id: int, db: Session = Depends(get_db), user=Depends(require_end_user)
):
    project = db.get(Project, project_id)
    if not project or project.owner_id != user.id:
        return {"deleted": False}
    log_action(db, user.id, "delete", "project", str(project_id), {})
    log_project_activity(
        db, project.id, user.id, "deleted", f"Project '{project.name}' deleted"
    )
    _notify_team_members(
        db,
        project,
        user.id,
        "Project deleted",
        f"The team project '{project.name}' was deleted.",
        "alert",
    )
    db.delete(project)
    db.commit()
    invalidate_prefix(f"projects:{user.id}:")
    return {"deleted": True}
