from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.dependencies.auth import get_current_user
from app.dependencies.roles import require_admin
from app.schemas.admin import AdminAnalyticsOut
from app.schemas.analytics import OwnerAnalyticsOut
from app.services.analytics_service import (get_admin_dashboard,
                                            get_owner_dashboard)

router = APIRouter(prefix="/analytics", tags=["Analytics"])


@router.get("/owner", response_model=OwnerAnalyticsOut)
def owner_dashboard(db: Session = Depends(get_db), user=Depends(get_current_user)):
    return get_owner_dashboard(db, user.id)


@router.get("/admin", response_model=AdminAnalyticsOut)
def admin_dashboard(db: Session = Depends(get_db), admin=Depends(require_admin)):
    return get_admin_dashboard(db)
