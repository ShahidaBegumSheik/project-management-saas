from pydantic import BaseModel, ConfigDict

class SubscriptionOut(BaseModel):
    plan: str
    status: str
    stripe_customer_id: str | None = None
    stripe_subscription_id: str | None = None

    model_config = ConfigDict(from_attributes=True)

