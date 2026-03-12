from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class ProjectCreate(BaseModel):
    name: str = Field(min_length=1, max_length=200)
    description: str | None = Field(default=None, max_length=1000)

    model_config = ConfigDict(
        json_schema_extra={"example": {"name": "FastAPI", "description": "Full Stack"}}
    )


class ProjectUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=200)
    description: str | None = Field(default=None, max_length=1000)
    team_id: int | None = None

    model_config = ConfigDict(
        json_schema_extra={
            "example": {"name": "FastAPI Updated", "description": "Updated Project"}
        }
    )


class ProjectOut(BaseModel):
    id: int
    name: str
    description: str | None
    team_id: int | None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class ProjectActivityOut(BaseModel):
    id: int
    project_id: int
    user_id: int
    action: str
    description: str
    timestamp: datetime
    model_config = ConfigDict(from_attributes=True)
