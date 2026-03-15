import enum
from datetime import datetime, timezone

from sqlalchemy import DateTime, Enum, ForeignKey, Index, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class Action(str, enum.Enum):
    created = "created"
    updated = "updated"
    deleted = "deleted"
    comment_added = "comment_added"


class ProjectActivity(Base):

    __tablename__ = "project_activities"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    project_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("projects.id", ondelete="CASCADE"), nullable=False
    )
    user_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    action: Mapped[Action] = mapped_column(Enum(Action), nullable=False)
    description: Mapped[str] = mapped_column(String(500), nullable=False)
    timestamp: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )

    project = relationship("Project", back_populates="activities")
    user = relationship("User", back_populates="activities")

    __table_args__ = (
        Index("ix_project_activity_project_time", "project_id", "timestamp"),
    )
