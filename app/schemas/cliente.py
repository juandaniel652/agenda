from pydantic import BaseModel, EmailStr

class ClienteBase(BaseModel):
    numero_cliente: str
    nombre: str
    apellido: str
    telefono: str
    domicilio: str
    numero_domicilio: str
    email: EmailStr


class ClienteCreate(ClienteBase):
    pass


class ClienteOut(ClienteBase):
    id: int

    class Config:
        from_attributes = True
