from pydantic import BaseModel
from uuid import UUID
from datetime import date, time
from enum import Enum


class EstadoTurnoEnum(str, Enum):
    abierto        = "Abierto"
    cerrado        = "Cerrado"
    reprogramacion = "Reprogramación"
    cancelado      = "Cancelado"


class TurnoBase(BaseModel):
    numero_ticket: str
    cliente_id:    UUID
    tecnico_id:    UUID
    tipo_turno:    int
    rango_horario: str
    estado:        EstadoTurnoEnum = EstadoTurnoEnum.abierto
    fecha:         date
    hora_inicio:   time
    hora_fin:      time


class TurnoCreate(TurnoBase):
    pass


class ClienteSimple(BaseModel):
    id:             UUID
    numero_cliente: str
    nombre:         str

    class Config:
        from_attributes = True


class TecnicoSimple(BaseModel):
    id:     UUID
    nombre: str

    class Config:
        from_attributes = True


class TurnoResponse(BaseModel):
    id:            UUID
    numero_ticket: str
    tipo_turno:    int
    rango_horario: str
    estado:        EstadoTurnoEnum
    fecha:         date
    hora_inicio:   time
    hora_fin:      time
    cliente:       ClienteSimple
    tecnico:       TecnicoSimple

    class Config:
        from_attributes = True