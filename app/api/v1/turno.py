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
from app.schemas.turno import TurnoResponse

router = APIRouter(prefix="/turnos", tags=["Turnos"])


@router.get("/", response_model=list[TurnoResponse])
def obtener_turnos(
    fecha: Optional[date] = Query(None),
    db: Session = Depends(get_db)
    ):

    query = select(Turno).where(
        Turno.estado != "cancelado"
    )

    if fecha:
        query = query.where(Turno.fecha == fecha)

    turnos = db.execute(query).scalars().all()

    return turnos


@router.post("/", response_model=TurnoResponse)
def crear_turno(turno: TurnoCreate, db: Session = Depends(get_db)):

    try:
        return TurnoService.crear(db, turno)

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.patch("/{turno_id}/cancelar")
def eliminar_turno(turno_id: UUID, db: Session = Depends(get_db)):

    try:
        TurnoService.eliminar(db, turno_id)
        return {"message": "Turno eliminado"}

    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))
