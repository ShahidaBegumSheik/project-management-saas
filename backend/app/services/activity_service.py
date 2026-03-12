from sqlalchemy.orm import Session

from app.models.project_activity import ProjectActivity


def log_project_activity(
    db: Session, project_id: int, user_id: int, action: str, description: str
):
    activity = ProjectActivity(
        project_id=project_id,
        user_id=user_id,
        action=action,
        description=description,
    )
    db.add(activity)
    return activity
