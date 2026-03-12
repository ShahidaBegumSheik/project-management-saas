from datetime import datetime, timezone

from sqlalchemy import DateTime, ForeignKey, Index, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class Team(Base):

    __tablename__ = "teams"

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, nullable=False, unique=True, index=True
    )
    name: Mapped[str] = mapped_column(String(80), nullable=False)
    description: Mapped[str | None] = mapped_column(String(500), nullable=True)
    owner_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    projects = relationship("Project", back_populates="team")
    owner = relationship("User", back_populates="owned_teams")
    members = relationship(
        "TeamMember", back_populates="team", cascade="all, delete-orphan"
    )
    invitations = relationship(
        "TeamInvitation", back_populates="team", cascade="all, delete-orphan"
    )

    __table_args__ = (Index("ix-team-owner-created", "owner_id", "created_at"),)
