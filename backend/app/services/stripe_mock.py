"""
Mock Stripe provider:
- Creates a "checkout session" URL that points to a frontend route.
- Simulates webhook events via a backend endpoint.
This keeps the same architecture as Stripe without requiring a Stripe account.
"""
import uuid

def create_checkout_session(user_id: int) -> dict:
    return {
        "id": f"cs_test_{uuid.uuid4().hex[:12]}",
        "url": f"http://localhost:5173/mock-checkout?user_id={user_id}"
    }

def create_portal_session(user_id: int) -> dict:
    return {
        "url": f"http://localhost:5173/mock-portal?user_id={user_id}"
    }