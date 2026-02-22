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


# ✅ agregar esto
class ClienteSimple(BaseModel):
    id: UUID
    nombre: str

    class Config:
        from_attributes = True


# ✅ agregar esto
class TecnicoSimple(BaseModel):
    id: UUID
    nombre: str

    class Config:
        from_attributes = True


# ✅ modificar esto
class TurnoResponse(BaseModel):

    id: UUID
    numero_ticket: str

    tipo_turno: TipoTurnoEnum
    estado: EstadoTurnoEnum

    fecha: date
    hora_inicio: time
    hora_fin: time

    cliente: ClienteSimple
    tecnico: TecnicoSimple

    class Config:
        from_attributes = True