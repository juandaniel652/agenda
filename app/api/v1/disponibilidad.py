from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.tecnico_disponibilidad import TecnicoDisponibilidad
from uuid import UUID

router = APIRouter()

@router.get("/tecnicos/{tecnico_id}/disponibilidad")
def obtener_disponibilidad(tecnico_id: UUID, db: Session = Depends(get_db)):
    horarios = db.query(TecnicoDisponibilidad)\
        .filter(TecnicoDisponibilidad.tecnico_id == tecnico_id)\
        .all()

    return horarios