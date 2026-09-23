from fastapi import APIRouter, Depends, HTTPException, status
from google.auth.transport import requests as google_requests
from google.oauth2 import id_token as google_id_token
from sqlalchemy import or_
from sqlalchemy.orm import Session

from app.config import settings
from app.database import get_db
from app.deps import get_current_user
from app.models import User
from app.schemas import AuthResponse, GoogleAuthRequest, LoginRequest, RegisterRequest, UserOut
from app.security import create_access_token, hash_password, verify_password

router = APIRouter(prefix="/api/auth", tags=["auth"])


@router.post("/register", response_model=AuthResponse, status_code=status.HTTP_201_CREATED)
def register(payload: RegisterRequest, db: Session = Depends(get_db)) -> AuthResponse:
    existing = db.query(User).filter(or_(User.email == payload.email, User.phone == payload.phone)).first()
    if existing is not None:
        detail = "Email already registered" if existing.email == payload.email else "Phone already registered"
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=detail)

    user = User(
        full_name=payload.full_name,
        email=payload.email,
        phone=payload.phone,
        password_hash=hash_password(payload.password),
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    token = create_access_token(str(user.id))
    return AuthResponse(access_token=token, user=UserOut.model_validate(user))


@router.post("/login", response_model=AuthResponse)
def login(payload: LoginRequest, db: Session = Depends(get_db)) -> AuthResponse:
    unauthorized = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password")

    user = db.query(User).filter(User.email == payload.email).first()
    if user is None or user.password_hash is None or not verify_password(payload.password, user.password_hash):
        raise unauthorized

    token = create_access_token(str(user.id))
    return AuthResponse(access_token=token, user=UserOut.model_validate(user))


@router.post("/google", response_model=AuthResponse)
def google_auth(payload: GoogleAuthRequest, db: Session = Depends(get_db)) -> AuthResponse:
    if not settings.google_client_id:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="Google sign-in is not configured")

    try:
        claims = google_id_token.verify_oauth2_token(
            payload.credential, google_requests.Request(), settings.google_client_id
        )
    except ValueError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Google credential")

    if not claims.get("email_verified", False):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Google email is not verified")

    google_id = claims["sub"]
    email = claims["email"]

    user = db.query(User).filter(User.google_id == google_id).first()
    if user is None:
        user = db.query(User).filter(User.email == email).first()
        if user is not None:
            user.google_id = google_id
        else:
            user = User(
                full_name=claims.get("name") or email.split("@")[0],
                email=email,
                google_id=google_id,
            )
            db.add(user)

    db.commit()
    db.refresh(user)

    token = create_access_token(str(user.id))
    return AuthResponse(access_token=token, user=UserOut.model_validate(user))


@router.get("/me", response_model=UserOut)
def me(current_user: User = Depends(get_current_user)) -> UserOut:
    return UserOut.model_validate(current_user)
