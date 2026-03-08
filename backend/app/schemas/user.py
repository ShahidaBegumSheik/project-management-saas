from datetime import datetime
from pydantic import BaseModel, EmailStr, ConfigDict

class UserOut(BaseModel):
    id: int
    email: EmailStr
    role: str
    is_active: bool
    stripe_customer_id: str | None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
        