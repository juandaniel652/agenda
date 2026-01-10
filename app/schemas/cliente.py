from pydantic import BaseModel, EmailStr
from uuid import UUID

class ClienteBase(BaseModel):
    numero_cliente: int
    nombre: str
    apellido: str
    telefono: str
    domicilio: str
    numero_domicilio: int
    email: EmailStr


class ClienteCreate(ClienteBase):
    pass


class ClienteOut(ClienteBase):
    id: UUID

    class Config:
        from_attributes = True
