from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

from app.schemas.auth import LoginSchema
from app.core.security import create_access_token, verify_password
from app.api.deps import get_db
from app.repositories.user_repository import UserRepository

from app.api.deps import get_current_user

from app.models.user import User

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

