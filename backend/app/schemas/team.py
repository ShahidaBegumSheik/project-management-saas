from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class TeamCreate(BaseModel):
    name: str = Field(min_length=1, max_length=80)
    description: str | None = Field(default=None, max_length=500)
    project_id: int

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "name": "Backend Team",
                "description": "Team for project collaboration",
                "project_id": 1,
            }
        }
    )


class TeamOut(BaseModel):
    id: int
    name: str
    description: str | None
    owner_id: int
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)


class TeamMemberOut(BaseModel):
    user_id: int
    email: EmailStr
    role: str


class TeamInvitationCreate(BaseModel):
    email: EmailStr


class TeamInvitationResponseIn(BaseModel):
    action: Literal["accept", "decline"]


class TeamInvitationOut(BaseModel):
    id: int
    team_id: int
    invited_email: EmailStr
    status: str
    invited_at: datetime
    responded_at: datetime | None = None
    model_config = ConfigDict(from_attributes=True)
