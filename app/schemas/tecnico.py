from pydantic import BaseModel, EmailStr
from uuid import UUID
from typing import List, Optional
from app.schemas.horario import HorarioBase

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
    horarios: Optional[List[HorarioBase]]   # 👈 ACÁ


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
