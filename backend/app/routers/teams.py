import secrets
from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.dependencies.auth import get_current_user
from app.dependencies.roles import (require_end_user,
                                    require_team_owner_or_admin)
from app.models.project import Project
from app.models.team import Team
from app.models.team_invitation import TeamInvitation, TeamInvitationStatus
from app.models.team_member import TeamMember, TeamMemberRole
from app.models.user import User
from app.schemas.team import (TeamCreate, TeamInvitationCreate,
                              TeamInvitationOut, TeamInvitationResponseIn,
                              TeamOut)
from app.services.audit_service import log_action
from app.services.email_service import send_team_invitation_email
from app.services.notification_service import (
    create_notification, create_notification_for_email_user)

router = APIRouter(prefix="/teams", tags=["Teams"])


@router.post("", response_model=TeamOut)
def create_team(
    payload: TeamCreate, db: Session = Depends(get_db), user=Depends(require_end_user)
):
    project = db.get(Project, payload.project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project Not Found")
    if project.owner_id != user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only the project owner can create a team for this project",
        )
    if project.team_id is not None:
        raise HTTPException(
            status_code=400, detail="A team is already associated with this project"
        )

    team = Team(name=payload.name, description=payload.description, owner_id=user.id)
    db.add(team)
    db.flush()

    db.add(TeamMember(team_id=team.id, user_id=user.id, role=TeamMemberRole.owner))

    project.team_id = team.id

    log_action(
        db,
        user.id,
        "team_created",
        "team",
        str(team.id),
        {"name": team.name, "project_id": project.id},
    )

    create_notification(
        db,
        user.id,
        "team created",
        f"Team '{team.name}' was created for project '{project.name}'.",
        "info",
    )
    db.commit()
    db.refresh(team)
    return team


@router.get("", response_model=list[TeamOut])
def list_teams(db: Session = Depends(get_db), user=Depends(get_current_user)):
    rows = (
        db.query(Team)
        .outerjoin(TeamMember, TeamMember.team_id == Team.id)
        .filter((Team.owner_id == user.id) | (TeamMember.user_id == user.id))
        .distinct()
        .order_by(Team.created_at.desc())
        .all()
    )
    return rows


@router.get("/{team_id}")
def team_detail(
    team_id: int, db: Session = Depends(get_db), user=Depends(get_current_user)
):
    team = db.get(Team, team_id)
    if not team:
        raise HTTPException(status_code=404, detail="Team not found")
    membership = (
        db.query(TeamMember)
        .filter(TeamMember.team_id == team_id, TeamMember.user_id == user.id)
        .first()
    )
    if team.owner_id != user.id and not membership:
        raise HTTPException(status_code=403, detail="Access denied")
    members = [
        {"user_id": m.user_id, "email": m.user.email, "role": m.role.value}
        for m in team.members
    ]
    projects = [
        {"id": p.id, "name": p.name, "description": p.description}
        for p in db.query(Project).filter(Project.team_id == team_id).all()
    ]
    invitations = [
        {"id": inv.id, "invited_email": inv.invited_email, "status": inv.status.value}
        for inv in team.invitations
    ]
    return {
        "team": team,
        "members": members,
        "projects": projects,
        "invitations": invitations,
    }


@router.post("/{team_id}/invite", response_model=TeamInvitationOut)
def invite_member(
    team_id: int,
    payload: TeamInvitationCreate,
    team=Depends(require_team_owner_or_admin),
    db: Session = Depends(get_db),
    user=Depends(require_end_user),
):
    normalized_email = payload.email.lower()
    existing_user = db.query(User).filter(User.email == normalized_email).first()
    if existing_user:
        existing_member = (
            db.query(TeamMember)
            .filter(
                TeamMember.team_id == team.id, TeamMember.user_id == existing_user.id
            )
            .first()
        )
        if existing_member:
            raise HTTPException(status_code=400, detail="User already belongs to team")

    pending = (
        db.query(TeamInvitation)
        .filter(
            TeamInvitation.team_id == team.id,
            TeamInvitation.invited_email == normalized_email,
            TeamInvitation.status == TeamInvitationStatus.pending,
        )
        .first()
    )
    if pending:
        raise HTTPException(status_code=400, detail="Pending invitation already exists")

    invitation = TeamInvitation(
        team_id=team.id,
        invited_user_id=existing_user.id if existing_user else None,
        inviter_user_id=user.id,
        invited_email=normalized_email,
        token=secrets.token_urlsafe(32),
        status=TeamInvitationStatus.pending,
        invited_at=datetime.now(timezone.utc),
    )
    db.add(invitation)

    frontend_invite_link = f"http://localhost:5173/app/teams?inviteToken={invitation.token}" 

    create_notification_for_email_user(
        db,
        normalized_email,
        "Team invitation",
        f"You have been invited to join {team.name}. Open this link to respond: {frontend_invite_link}",
        "info",
    )

    if existing_user:
        create_notification(
            db,existing_user.id, "Team invitation",
            f"You have been invited to join {team.name}. Open this link to respond: {frontend_invite_link}",
            "info",
        )
    try:
        send_team_invitation_email(
            normalized_email,
            team.name,
            frontend_invite_link,
        )
    except Exception as e:
        print(f"Team invitation email failed: {e}")
        
    log_action(
        db,
        user.id,
        "team_invitation_sent",
        "team",
        str(team.id),
        {"email": normalized_email},
    )
    db.commit()
    db.refresh(invitation)
    return invitation


@router.post("/invitations/{token}")
def respond_to_invitation(
    token: str,
    payload: TeamInvitationResponseIn,
    db: Session = Depends(get_db),
    user=Depends(require_end_user),
):
    invitation = db.query(TeamInvitation).filter(TeamInvitation.token == token).first()
    if not invitation or invitation.invited_email.lower() != user.email.lower():
        raise HTTPException(status_code=404, detail="Invitation not found")
    if invitation.status != TeamInvitationStatus.pending:
        raise HTTPException(status_code=400, detail="Invitation already responded")
    invitation.responded_at = datetime.now(timezone.utc)
    if payload.action == "accept":
        invitation.status = TeamInvitationStatus.accepted
        already_member = (
            db.query(TeamMember)
            .filter(
                TeamMember.team_id == invitation.team_id, TeamMember.user_id == user.id
            )
            .first()
        )
        if not already_member:
            db.add(
                TeamMember(
                    team_id=invitation.team_id,
                    user_id=user.id,
                    role=TeamMemberRole.member,
                )
            )
        create_notification(
            db,
            invitation.team.owner_id,
            "Invitation accepted",
            f"{user.email} accepted the invitation to join {invitation.team.name}.",
            "info",
        )
    else:
        invitation.status = TeamInvitationStatus.declined
        create_notification(
            db,
            invitation.team.owner_id,
            "Invitation declined",
            f"{user.email} declined the invitation to join {invitation.team.name}.",
            "alert",
        )
    log_action(
        db,
        user.id,
        f"team_invitation_{payload.action}ed",
        "team",
        str(invitation.team_id),
        {"invitation_id": invitation.id},
    )
    db.commit()
    return {"message": f"Invitation {payload.action}ed successfully"}


@router.delete("/{team_id}/members/{member_user_id}")
def remove_member(
    team_id: int,
    member_user_id: int,
    team=Depends(require_team_owner_or_admin),
    db: Session = Depends(get_db),
    user=Depends(require_end_user),
):
    membership = (
        db.query(TeamMember)
        .filter(TeamMember.team_id == team.id, TeamMember.user_id == member_user_id)
        .first()
    )
    if not membership:
        raise HTTPException(status_code=404, detail="Member not found")
    if membership.role == TeamMemberRole.owner:
        raise HTTPException(status_code=400, detail="Cannot remove owner membership")
    db.delete(membership)
    create_notification(
        db,
        member_user_id,
        "Removed from team",
        f"You have been removed from team {team.name}.",
        "alert",
    )
    log_action(
        db,
        user.id,
        "team_member_removed",
        "team",
        str(team.id),
        {"member_user_id": member_user_id},
    )
    db.commit()
    return {"removed": True}
