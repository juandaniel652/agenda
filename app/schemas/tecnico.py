from pydantic import BaseModel, EmailStr
from typing import Optional
from uuid import UUID

class TecnicoCreate(BaseModel):
    email: Optional[EmailStr]
    nombre: str
    apellido: str
    telefono: Optional[str]
    duracion_turno_min: int
    imagen_url: Optional[str]

class TecnicoUpdate(BaseModel):
    email: Optional[EmailStr]
    nombre: Optional[str]
    apellido: Optional[str]
    telefono: Optional[str]
    duracion_turno_min: Optional[int]
    imagen_url: Optional[str]
    activo: Optional[bool]

class TecnicoOut(BaseModel):
    id: UUID
    email: Optional[EmailStr]
    nombre: str
    apellido: str
    telefono: Optional[str]
    duracion_turno_min: int
    imagen_url: Optional[str]
    activo: bool

    class Config:
        from_attributes = True
