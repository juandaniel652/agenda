from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import select
from uuid import UUID
from datetime import date
from typing import Optional
from pydantic import BaseModel

from app.db.session import get_db
from app.schemas.turno import TurnoCreate, TurnoResponse, EstadoTurnoEnum
from app.services.turno_service import TurnoService
from app.models.turno import Turno

router = APIRouter(prefix="/turnos", tags=["Turnos"])


class PatchEstadoSchema(BaseModel):
    estado: EstadoTurnoEnum


@router.get("/", response_model=list[TurnoResponse])
def obtener_turnos(
    fecha: Optional[date] = Query(None),
    db: Session = Depends(get_db),
):
    query = select(Turno)
    if fecha:
        query = query.where(Turno.fecha == fecha)

    turnos = db.execute(query).scalars().all()
    return [t for t in turnos if t.estado != "Cancelado"]


@router.post("/", response_model=TurnoResponse)
def crear_turno(turno: TurnoCreate, db: Session = Depends(get_db)):
    try:
        return TurnoService.crear(db, turno)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.patch("/{turno_id}/estado", response_model=TurnoResponse)
def actualizar_estado_turno(
    turno_id: UUID,
    body: PatchEstadoSchema,
    db: Session = Depends(get_db),
):
    turno = db.query(Turno).filter(Turno.id == turno_id).first()
    if not turno:
        raise HTTPException(status_code=404, detail="Turno no encontrado")
    turno.estado = body.estado.value  # ← .value para que SQLAlchemy reciba el string
    db.commit()
    db.refresh(turno)
    return turno


@router.patch("/{turno_id}/cancelar")
def cancelar_turno(
    turno_id: UUID,
    db: Session = Depends(get_db),
):
    try:
        TurnoService.eliminar(db, turno_id)
        return {"message": "Turno cancelado"}
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))