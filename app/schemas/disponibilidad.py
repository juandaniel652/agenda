from pydantic import BaseModel
from uuid import UUID

class DisponibilidadBase(BaseModel):
    dia_semana: int
    hora_inicio: str   # "HH:MM:SS"
    hora_fin: str      # "HH:MM:SS"

class DisponibilidadCreate(DisponibilidadBase):
    tecnico_id: UUID

class DisponibilidadUpdate(DisponibilidadBase):
    pass

class DisponibilidadOut(DisponibilidadBase):
    id: UUID
    tecnico_id: UUID

    class Config:
        orm_mode = True