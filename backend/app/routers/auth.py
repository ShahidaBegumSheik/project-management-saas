import secrets

from fastapi import APIRouter, Depends, HTTPException, Query, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.database import get_db
from app.core.security import (create_access_token, create_refresh_token,
                               decode_token, hash_password, verify_password)
from app.dependencies.auth import get_current_user
from app.models.refresh_token import RefreshToken
from app.models.user import User, UserRole
from app.schemas.auth import (LoginIn, RefreshTokenIn, RegisterIn, RegisterOut,
                              TokenOut, UserMeOut, VerifyEmailOut)
from app.services.audit_service import log_action
from app.services.email_service import send_verification_email
from app.services.notification_service import create_notification
from app.services.rate_limit_service import check_rate_limit, reset_rate_limit
from app.services.subscription_service import get_or_create_subscription

router = APIRouter(prefix="/auth", tags=["Auth"])


def _issue_tokens(user: User, db: Session) -> TokenOut:
    access = create_access_token(subject=str(user.id), extra={"role": user.role.value})
    refresh_token, expires_at = create_refresh_token(subject=str(user.id))
    db.add(RefreshToken(user_id=user.id, token=refresh_token, expires_at=expires_at))
    log_action(db, user.id, "login", "user", str(user.id), {})
    db.commit()
    return TokenOut(access_token=access, refresh_token=refresh_token)


@router.post("/register", response_model=RegisterOut)
def register(payload: RegisterIn, db: Session = Depends(get_db)):
    normalized_email = payload.email.lower()
    existing = db.query(User).filter(User.email == normalized_email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")

    token = secrets.token_urlsafe(32)
    user = User(
        email=normalized_email,
        hashed_password=hash_password(payload.password),
        role=UserRole.user,
        verification_token=token,
        email_verified=False,
    )

    if settings.seed_admin and user.email == settings.admin_email.lower():
        user.role = UserRole.admin
        user.email_verified = True
        user.verification_token = None

    db.add(user)
    db.flush()

    get_or_create_subscription(db, user.id)
    log_action(db, user.id, "register", "user", str(user.id), {"email": user.email})

    if not user.email_verified:
        verify_url = f"{settings.frontend_verify_url}?token={token}"
        try:
            send_verification_email(user.email, verify_url)
            create_notification(
                db,
                user.id,
                "Verify your email",
                "Please verify your email address to activate your account.",
                "system",
            )
        except Exception as e:
            print(f"Verification email failed: {e}")

    db.commit()
    return RegisterOut(
        message="Registration successful. Please verify your email.",
        email=user.email,
        verification_required=not user.email_verified,
        verification_token=token if not user.email_verified else None,
    )


@router.get("/verify-email", response_model=VerifyEmailOut)
def verify_email(token: str = Query(...), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.verification_token == token).first()
    if not user:
        raise HTTPException(status_code=400, detail="Invalid verification token")
    user.email_verified = True
    user.verification_token = None
    create_notification(
        db,
        user.id,
        "Email verified",
        "Your email has been verified successfully.",
        "system",
    )
    log_action(db, user.id, "email_verified", "user", str(user.id), {})
    db.commit()
    return VerifyEmailOut(message="Email verified successfully. You can now log in.")


def _authenticate(email: str, password: str, db: Session):
    normalized_email = email.lower()
    check_rate_limit(normalized_email)
    user = db.query(User).filter(User.email == normalized_email).first()
    if not user or not verify_password(password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials"
        )
    if not user.email_verified:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Please verify your email before logging in",
        )
    reset_rate_limit(normalized_email)
    return user


@router.post("/login", response_model=TokenOut)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    user = _authenticate(form_data.username, form_data.password, db)
    return _issue_tokens(user, db)


@router.post("/login-json", response_model=TokenOut)
def login_json(payload: LoginIn, db: Session = Depends(get_db)):
    user = _authenticate(payload.email, payload.password, db)
    return _issue_tokens(user, db)


@router.post("/refresh", response_model=TokenOut)
def refresh_token(payload: RefreshTokenIn, db: Session = Depends(get_db)):
    try:
        claims = decode_token(payload.refresh_token)
        if claims.get("type") != "refresh":
            raise ValueError("Invalid refresh token")
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid refresh token")
    stored = (
        db.query(RefreshToken)
        .filter(
            RefreshToken.token == payload.refresh_token,
            RefreshToken.is_revoked.is_(False),
        )
        .first()
    )
    if not stored:
        raise HTTPException(status_code=401, detail="Refresh token not found")
    user = db.get(User, stored.user_id)
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    stored.is_revoked = True
    access = create_access_token(subject=str(user.id), extra={"role": user.role.value})
    refresh, expires_at = create_refresh_token(subject=str(user.id))
    db.add(RefreshToken(user_id=user.id, token=refresh, expires_at=expires_at))
    db.commit()
    return TokenOut(access_token=access, refresh_token=refresh)


@router.get("/me", response_model=UserMeOut)
def me(user=Depends(get_current_user)):
    return user
