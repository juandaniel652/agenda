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

    email: Optional[EmailStr] = None
    nombre: Optional[str] = None
    apellido: Optional[str] = None
    telefono: Optional[str] = None
    duracion_turno_min: Optional[int] = None
    imagen_url: Optional[str] = None
    activo: Optional[bool] = None
    horarios: Optional[List[HorarioBase]] = None



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
