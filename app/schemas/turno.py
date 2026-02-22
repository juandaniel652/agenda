from pydantic import BaseModel
from uuid import UUID
from datetime import date, time
from enum import Enum

class TurnoBase(BaseModel):
    numero_ticket: str
    cliente_id: UUID
    tecnico_id: UUID
    tipo_turno: str
    estado: str = "pendiente"
    fecha: date
    hora_inicio: time
    hora_fin: time


class TurnoCreate(TurnoBase):
    pass


class TurnoResponse(TurnoBase):
    id: UUID

    class Config:
        from_attributes = True


class TipoTurnoEnum(str, Enum):
    regular = "regular"
    urgente = "urgente"


class EstadoTurnoEnum(str, Enum):
    pendiente = "pendiente"
    confirmado = "confirmado"
    cancelado = "cancelado"
    completado = "completado"