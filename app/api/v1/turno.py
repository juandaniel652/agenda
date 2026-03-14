from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from uuid import UUID
from app.db.session import get_db
from app.schemas.turno import TurnoCreate, TurnoResponse
from app.services.turno_service import TurnoService
from datetime import date
from typing import Optional
from sqlalchemy import select
from app.models.turno import Turno
from enum import Enum
from pydantic import BaseModel

router = APIRouter(prefix="/turnos", tags=["Turnos"])

class EstadoTicket(str, Enum):
    abierto        = "Abierto"
    cerrado        = "Cerrado"
    reprogramacion = "Reprogramación"
    cancelado      = "Cancelado"

class PatchEstadoSchema(BaseModel):
    estado: EstadoTicket

@router.get("/", response_model=list[TurnoResponse])
def obtener_turnos(
    fecha: Optional[date] = Query(None),
    db: Session = Depends(get_db),
):
    query = select(Turno).where(Turno.estado != "cancelado")
    if fecha:
        query = query.where(Turno.fecha == fecha)
    return db.execute(query).scalars().all()

@router.post("/", response_model=TurnoResponse)
def crear_turno(turno: TurnoCreate, db: Session = Depends(get_db)):
    try:
        return TurnoService.crear(db, turno)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.patch("/{turno_id}/estado")
def actualizar_estado_turno(
    turno_id: UUID,           # ← ajustá a int si tu PK es int
    body: PatchEstadoSchema,
    db: Session = Depends(get_db),
):
    turno = db.query(Turno).filter(Turno.id == turno_id).first()
    if not turno:
        raise HTTPException(status_code=404, detail="Turno no encontrado")
    turno.estado = body.estado
    db.commit()
    db.refresh(turno)
    return turno

@router.patch("/{turno_id}/cancelar")
def cancelar_turno(
    turno_id: UUID,           # ← mismo tipo que arriba
    db: Session = Depends(get_db),
):
    try:
        TurnoService.eliminar(db, turno_id)
        return {"message": "Turno eliminado"}
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))