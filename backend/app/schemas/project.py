from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime

class ProjectCreate(BaseModel):
    name: str = Field(min_length=1, max_length=200)
    description: str | None = Field(default=None, max_length=1000)

class ProjectOut(BaseModel):
    id: int
    name: str
    description: str | None
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)