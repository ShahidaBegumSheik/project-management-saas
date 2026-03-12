from sqlalchemy.orm import Session

from app.models.notification import Notification, NotificationType
from app.models.user import User


def create_notification(
    db: Session, user_id: int, title: str, message: str, type_: str = "info"
) -> Notification:
    notif = Notification(
        user_id=user_id,
        title=title,
        message=message,
        type=NotificationType(type_),
        is_read=False,
    )
    db.add(notif)
    return notif


def create_notification_for_email_user(
    db: Session, email: str, title: str, message: str, type_: str = "info"
) -> None:
    user = db.query(User).filter(User.email == email).first()
    if user:
        create_notification(db, user.id, title, message, type_)
