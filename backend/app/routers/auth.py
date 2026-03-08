from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import hash_password, verify_password, create_access_token
from app.schemas.auth import RegisterIn, TokenOut, LoginIn

from app.models.user import User, UserRole
from app.services.subscription_service import get_or_create_subscription
from app.services.audit_service import log_action
from app.core.config import settings

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/register", response_model=TokenOut)
def register(payload: RegisterIn, db: Session = Depends(get_db)):
    existing = db.query(User).filter(User.email == payload.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")

    user = User(email=payload.email, 
                hashed_password=hash_password(payload.password), 
                role=UserRole.user)
    
    db.add(user)
    db.flush()

    get_or_create_subscription(db, user.id)
    log_action(db, user.id, "register", "user", str(user.id), {"email": user.email})

    if settings.seed_admin and user.email == settings.admin_email:
        user.role = UserRole.admin

    db.commit()
    return TokenOut(access_token=create_access_token(subject=str(user.id), extra={"role": user.role.value}))


def _build_token_response(user: User, db: Session):
    log_action(db, user.id, "login", "user", str(user.id), {})
    db.commit()
    return TokenOut(
        access_token=create_access_token(
            subject=str(user.id),
            extra={"role": user.role.value if hasattr(user.role, "value") else str(user.role)},
        )
    )

@router.post("/login")
def login(
	form_data: OAuth2PasswordRequestForm = Depends(),
	db: Session = Depends(get_db),
):
     user = db.query(User).filter(User.email == form_data.username).first()
     if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
     token = create_access_token(
    	subject=str(user.id),
    	extra={"role": user.role.value if hasattr(user.role, "value") else str(user.role)},)
     return _build_token_response(user, db)
 

@router.post("/login-json", response_model=TokenOut)
def login_json(payload: LoginIn, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == payload.email).first()
    if not user or not verify_password(payload.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    return _build_token_response(user, db)
