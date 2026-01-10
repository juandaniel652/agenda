from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_db, get_current_user
from app.models.user import User
from app.models.cliente import Cliente

router = APIRouter(
    prefix="/clientes",
    tags=["Clientes"]
)


@router.get("/")
def listar_clientes(
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):
    clientes = db.query(Cliente).all()
    return {
        "data": clientes,
        "count": len(clientes)
    }
