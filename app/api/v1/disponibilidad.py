from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import UUID

from app.db.session import get_db
from app.services.disponibilidad_service import (
    get_disponibilidad,
    create_disponibilidad,
    update_disponibilidad,
    delete_disponibilidad
)
from app.schemas.disponibilidad import (
    DisponibilidadCreate,
    DisponibilidadUpdate,
    DisponibilidadOut
)

router = APIRouter()

@router.get("/tecnicos/{tecnico_id}/disponibilidad", response_model=list[DisponibilidadOut])
def api_get_disponibilidad(tecnico_id: UUID, db: Session = Depends(get_db)):
    return get_disponibilidad(db, tecnico_id)

@router.post("/tecnicos/{tecnico_id}/disponibilidad", response_model=DisponibilidadOut)
def api_create_disponibilidad(tecnico_id: UUID, data: DisponibilidadCreate, db: Session = Depends(get_db)):
    if tecnico_id != data.tecnico_id:
        raise HTTPException(status_code=400, detail="ID técnico mismatch")
    return create_disponibilidad(db, data)

@router.put("/disponibilidad/{dispo_id}", response_model=DisponibilidadOut)
def api_update_disponibilidad(dispo_id: UUID, data: DisponibilidadUpdate, db: Session = Depends(get_db)):
    updated = update_disponibilidad(db, dispo_id, data)
    if not updated:
        raise HTTPException(status_code=404, detail="Disponibilidad no encontrada")
    return updated

@router.delete("/disponibilidad/{dispo_id}")
def api_delete_disponibilidad(dispo_id: UUID, db: Session = Depends(get_db)):
    success = delete_disponibilidad(db, dispo_id)
    if not success:
        raise HTTPException(status_code=404, detail="Disponibilidad no encontrada")
    return {"detail": "Eliminado correctamente"}