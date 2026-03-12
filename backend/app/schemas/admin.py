from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr


class AdminUserOut(BaseModel):
    id: int
    email: EmailStr
    role: str
    is_active: bool
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)


class AdminSubscriptionOut(BaseModel):
    id: int
    user_id: int
    plan: str
    status: str
    stripe_customer_id: str | None
    stripe_subscription_id: str | None
    model_config = ConfigDict(from_attributes=True)


class UserSubscriptionMapOut(BaseModel):
    user_id: int
    email: EmailStr
    plan: str
    status: str


class AdminAnalyticsOut(BaseModel):
    total_users: int
    free_users: int
    pro_users: int
    active_subscriptions: int
    registrations_this_month: int
    teams_count: int
    unread_notifications: int
