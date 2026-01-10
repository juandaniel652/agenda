from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import UUID

from app.api.deps import get_db, get_current_user
from app.models.cliente import Cliente
from app.schemas.cliente import ClienteCreate, ClienteOut
from app.models.user import User

router = APIRouter(prefix="/clientes", tags=["Clientes"])


@router.get("/", response_model=list[ClienteOut])
def listar_clientes(
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):
    return db.query(Cliente).all()


@router.post("/", response_model=ClienteOut, status_code=201)
def crear_cliente(
    cliente: ClienteCreate,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):
    nuevo = Cliente(**cliente.model_dump())
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return nuevo


@router.put("/{cliente_id}", response_model=ClienteOut)
def actualizar_cliente(
    cliente_id: UUID,
    datos: ClienteCreate,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):
    cliente = db.get(Cliente, cliente_id)
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")

    for campo, valor in datos.model_dump().items():
        setattr(cliente, campo, valor)

    db.commit()
    db.refresh(cliente)
    return cliente


@router.delete("/{cliente_id}", status_code=204)
def eliminar_cliente(
    cliente_id: UUID,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):
    cliente = db.get(Cliente, cliente_id)
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")

    db.delete(cliente)
    db.commit()
