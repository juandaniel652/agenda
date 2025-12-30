from pydantic import BaseModel, EmailStr

class ClienteBase(BaseModel):
    nombre: str
    email: EmailStr

class ClienteCreate(ClienteBase):
    pass

class ClienteOut(ClienteBase):
    id: int

    class Config:
        from_attributes = True
