from pydantic import BaseModel
from uuid import UUID
from datetime import date, time
from enum import Enum


class TipoTurnoEnum(str, Enum):
    consulta = "consulta"
    control = "control"
    urgencia = "urgencia"


class EstadoTurnoEnum(str, Enum):
    pendiente = "pendiente"
    confirmado = "confirmado"
    cancelado = "cancelado"
    completado = "completado"


class TurnoBase(BaseModel):
    numero_ticket: str
    cliente_id: UUID
    tecnico_id: UUID
    tipo_turno: TipoTurnoEnum
    estado: EstadoTurnoEnum = EstadoTurnoEnum.pendiente
    fecha: date
    hora_inicio: time
    hora_fin: time


class TurnoCreate(TurnoBase):
    pass


class TurnoResponse(TurnoBase):
    id: UUID

    class Config:
        from_attributes = True