from pydantic import BaseModel, EmailStr

class ClienteCreate(BaseModel):
    numero_cliente: str
    nombre: str
    apellido: str
    telefono: str
    domicilio: str
    numero_domicilio: str
    email: EmailStr

class ClienteOut(ClienteCreate):
    id: int

    class Config:
        from_attributes = True
