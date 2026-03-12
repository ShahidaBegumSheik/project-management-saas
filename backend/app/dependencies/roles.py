from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.dependencies.auth import get_current_user
from app.models.project import Project
from app.models.team import Team
from app.models.team_member import TeamMember
from app.models.user import UserRole


def require_admin(user=Depends(get_current_user)):
    if user.role != UserRole.admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Admin only")
    return user


def require_end_user(user=Depends(get_current_user)):
    if user.role != UserRole.user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only users can perform this action",
        )
    return user


def require_team_owner_or_admin(
    team_id: int, user=Depends(get_current_user), db: Session = Depends(get_db)
):
    team = db.get(Team, team_id)
    if not team:
        raise HTTPException(status_code=404, detail="Team not found")
    if user.role == UserRole.admin or team.owner_id == user.id:
        return team
    raise HTTPException(status_code=403, detail="Only team owner can manage members")


def require_project_or_admin(
    project_id: int, user=Depends(get_current_user), db: Session = Depends(get_db)
):
    project = db.get(Project, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    if user.role == UserRole.admin or project.owner_id == user.id:
        return project
    raise HTTPException(
        status_code=403, detail="Only project owner can perform this action"
    )


def can_access_team_project(project: Project, user, db: Session):
    if user.role == UserRole.admin or project.owner_id == user.id:
        return True
    if project.team_id is None:
        return False
    membership = (
        db.query(TeamMember)
        .filter(
            TeamMember.team_id == project.team_id,
            TeamMember.user_id == user.id,
        )
        .first()
    )
    return membership is not None
