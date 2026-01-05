from pydantic import BaseModel, EmailStr

class TecnicoCreate(BaseModel):
    email: EmailStr
    password: str
    nombre: str | None = None
