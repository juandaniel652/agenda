from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import UUID

from app.db.session import get_db
from app.schemas.turno import TurnoCreate, TurnoResponse
from app.services.turno_service import TurnoService

router = APIRouter(prefix="/turnos", tags=["Turnos"])


@router.get("/", response_model=list[TurnoResponse])
def obtener_turnos(db: Session = Depends(get_db)):

    return TurnoService.obtener_todos(db)


@router.post("/", response_model=TurnoResponse)
def crear_turno(turno: TurnoCreate, db: Session = Depends(get_db)):

    try:
        return TurnoService.crear(db, turno)

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/{turno_id}")
def eliminar_turno(turno_id: UUID, db: Session = Depends(get_db)):

    try:
        TurnoService.eliminar(db, turno_id)
        return {"message": "Turno eliminado"}

    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))
