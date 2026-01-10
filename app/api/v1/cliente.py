from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_db, get_current_user
from app.models.user import User
from app.models.cliente import Cliente
from app.schemas.cliente import ClienteCreate, ClienteOut

router = APIRouter(
    prefix="/clientes",
    tags=["Clientes"]
)

@router.get("/", response_model=list[ClienteOut])
def listar_clientes(
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):
    return db.query(Cliente).all()


@router.post(
    "/",
    response_model=ClienteOut,
    status_code=status.HTTP_201_CREATED
)
def crear_cliente(
    cliente: ClienteCreate,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):
    existe = db.query(Cliente).filter(
        Cliente.numero_cliente == cliente.numero_cliente
    ).first()

    if existe:
        raise HTTPException(
            status_code=400,
            detail="El número de cliente ya existe"
        )

    nuevo = Cliente(**cliente.model_dump())

    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)

    return nuevo
