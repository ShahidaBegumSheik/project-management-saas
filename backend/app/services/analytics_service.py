from datetime import datetime, timezone

from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.notification import Notification
from app.models.project import Project
from app.models.project_activity import ProjectActivity
from app.models.subscription import Subscription
from app.models.team import Team
from app.models.team_member import TeamMember
from app.models.user import User


def get_owner_dashboard(db: Session, user_id: int):
    total_projects = (
        db.query(func.count(Project.id)).filter(Project.owner_id == user_id).scalar()
        or 0
    )
    subscription = (
        db.query(Subscription).filter(Subscription.user_id == user_id).first()
    )
    team_members_count = (
        db.query(func.count(TeamMember.id))
        .join(Team, Team.id == TeamMember.team_id)
        .filter(Team.owner_id == user_id)
        .scalar()
        or 0
    )
    recent_project_activity = (
        db.query(func.count(ProjectActivity.id))
        .join(Project, Project.id == ProjectActivity.project_id)
        .filter(Project.owner_id == user_id)
        .scalar()
        or 0
    )
    unread_notifications = (
        db.query(func.count(Notification.id))
        .filter(Notification.user_id == user_id, Notification.is_read.is_(False))
        .scalar()
        or 0
    )
    return {
        "total_projects": total_projects,
        "active_subscription_status": subscription.status if subscription else "active",
        "team_members_count": max(team_members_count - 1, 0),
        "recent_project_activity": recent_project_activity,
        "unread_notifications": unread_notifications,
    }


def get_admin_dashboard(db: Session):
    now = datetime.now(timezone.utc)
    month_start = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    total_users = db.query(func.count(User.id)).scalar() or 0
    free_users = (
        db.query(func.count(Subscription.id))
        .filter(Subscription.plan == "free")
        .scalar()
        or 0
    )
    pro_users = (
        db.query(func.count(Subscription.id))
        .filter(Subscription.plan == "pro")
        .scalar()
        or 0
    )
    active_subscriptions = (
        db.query(func.count(Subscription.id))
        .filter(Subscription.status == "active", Subscription.plan == "pro")
        .scalar()
        or 0
    )
    registrations_this_month = (
        db.query(func.count(User.id)).filter(User.created_at >= month_start).scalar()
        or 0
    )
    teams_count = db.query(func.count(Team.id)).scalar() or 0
    unread_notifications = (
        db.query(func.count(Notification.id))
        .filter(Notification.is_read.is_(False))
        .scalar()
        or 0
    )
    return {
        "total_users": total_users,
        "free_users": free_users,
        "pro_users": pro_users,
        "active_subscriptions": active_subscriptions,
        "registrations_this_month": registrations_this_month,
        "teams_count": teams_count,
        "unread_notifications": unread_notifications,
    }
