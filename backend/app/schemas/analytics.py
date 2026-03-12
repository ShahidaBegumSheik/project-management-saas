from pydantic import BaseModel


class OwnerAnalyticsOut(BaseModel):
    total_projects: int
    active_subscription_status: str
    team_members_count: int
    recent_project_activity: int
    unread_notifications: int
