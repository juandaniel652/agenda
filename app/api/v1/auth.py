from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

from app.schemas.auth import LoginSchema
from app.core.security import create_access_token, verify_password
from app.api.deps import get_db
from app.repositories.user_repository import UserRepository

from app.api.deps import get_current_user

from app.models.user import User

from app.schemas.auth import RegisterSchema, ForgotPasswordSchema, ResetPasswordSchema
from app.core.security import hash_password

import secrets
from datetime import datetime, timedelta

from app.core.email import send_reset_email



router = APIRouter(prefix="/auth", tags=["Auth"])

@router.get("/ping")
def auth_ping():
    return {"auth": "ok"}


@router.post("/login")
def login(data: LoginSchema, db: Session = Depends(get_db)):

    user = UserRepository.get_by_email(db, data.email)

    if not user:
        raise HTTPException(status_code=401, detail="Credenciales inválidas")

    if not user.is_active:
        raise HTTPException(status_code=403, detail="Usuario deshabilitado")

    if not verify_password(data.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Credenciales inválidas")

    access_token = create_access_token({
        "sub": str(user.id),
        "email": user.email,
        "role": user.role
    })

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }
    

@router.get("/me")
def me(current_user: User = Depends(get_current_user)):
    return {
        "id": current_user.id,
        "email": current_user.email,
        "role": current_user.role,
        "is_active": current_user.is_active
    }


@router.post("/register")
def register(data: RegisterSchema, db: Session = Depends(get_db)):

    existing = UserRepository.get_by_email(db, data.email)

    if existing:
        raise HTTPException(status_code=400, detail="El email ya está registrado")

    user = User(
        email=data.email,
        password_hash=hash_password(data.password),
        role="user"
    )

    user = UserRepository.create(db, user)

    return {
        "message": "Usuario creado",
        "id": user.id,
        "email": user.email
    }


@router.post("/forgot-password")
async def forgot_password(data: ForgotPasswordSchema, db: Session = Depends(get_db)):

    user = UserRepository.get_by_email(db, data.email)

    if not user:
        return {"message": "Si el email existe, recibirás instrucciones"}

    token = secrets.token_urlsafe(32)

    user.reset_token = token
    user.reset_token_expire = datetime.utcnow() + timedelta(hours=1)

    db.commit()

    await send_reset_email(user.email, token)

    return {
        "message": "Si el email existe, recibirás instrucciones"
    }

    user = UserRepository.get_by_email(db, data.email)

    if not user:
        return {"message": "Si el email existe, recibirás instrucciones"}

    token = secrets.token_urlsafe(32)

    user.reset_token = token
    user.reset_token_expire = datetime.utcnow() + timedelta(hours=1)

    db.commit()

    return {
        "message": "Token generado",
        "reset_token": token
    }

@router.post("/reset-password")
def reset_password(data: ResetPasswordSchema, db: Session = Depends(get_db)):

    user = db.query(User).filter(User.reset_token == data.token).first()

    if not user:
        raise HTTPException(status_code=400, detail="Token inválido")

    if user.reset_token_expire < datetime.utcnow():
        raise HTTPException(status_code=400, detail="Token expirado")

    user.password_hash = hash_password(data.password)

    user.reset_token = None
    user.reset_token_expire = None

    db.commit()

    return {"message": "Contraseña actualizada"}