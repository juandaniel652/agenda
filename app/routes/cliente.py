from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.dependencies import get_db
from app.models.cliente import Cliente
from app.schemas.cliente import ClienteCreate, ClienteOut

router = APIRouter(
    prefix="/clientes",
    tags=["Clientes"]
)

@router.post(
    "/",
    response_model=ClienteOut,
    status_code=status.HTTP_201_CREATED
)
def crear_cliente(
    cliente: ClienteCreate,
    db: Session = Depends(get_db)
):
    existe = db.query(Cliente).filter(Cliente.email == cliente.email).first()
    if existe:
        raise HTTPException(
            status_code=400,
            detail="El email ya está registrado"
        )

    nuevo_cliente = Cliente(
        nombre=cliente.nombre,
        email=cliente.email
    )

    db.add(nuevo_cliente)
    db.commit()
    db.refresh(nuevo_cliente)

    return nuevo_cliente


@router.get(
    "/",
    response_model=list[ClienteOut]
)
def listar_clientes(db: Session = Depends(get_db)):
    return db.query(Cliente).all()

@router.post("/", response_model=ClienteOut, status_code=201)
def crear_cliente(cliente: ClienteCreate, db: Session = Depends(get_db)):
    existe = db.query(Cliente).filter(Cliente.email == cliente.email).first()
    if existe:
        raise HTTPException(status_code=400, detail="El email ya está registrado")

    nuevo = Cliente(
        numero_cliente=cliente.numero_cliente,
        nombre=cliente.nombre,
        apellido=cliente.apellido,
        telefono=cliente.telefono,
        domicilio=cliente.domicilio,
        numero_domicilio=cliente.numero_domicilio,
        email=cliente.email
    )

    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return nuevo
