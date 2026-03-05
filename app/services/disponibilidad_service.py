from sqlalchemy.orm import Session
from app.models.tecnico_disponibilidad import TecnicoDisponibilidad
from uuid import UUID
from app.schemas.disponibilidad import DisponibilidadCreate, DisponibilidadUpdate

def get_disponibilidad(db: Session, tecnico_id: UUID):
    return db.query(TecnicoDisponibilidad).filter_by(tecnico_id=tecnico_id).all()

def create_disponibilidad(db: Session, data: DisponibilidadCreate):
    dispo = TecnicoDisponibilidad(**data.dict())
    db.add(dispo)
    db.commit()
    db.refresh(dispo)
    return dispo

def update_disponibilidad(db: Session, dispo_id: UUID, data: DisponibilidadUpdate):
    dispo = db.query(TecnicoDisponibilidad).get(dispo_id)
    if not dispo:
        return None
    for field, value in data.dict().items():
        setattr(dispo, field, value)
    db.commit()
    db.refresh(dispo)
    return dispo

def delete_disponibilidad(db: Session, dispo_id: UUID):
    dispo = db.query(TecnicoDisponibilidad).get(dispo_id)
    if not dispo:
        return False
    db.delete(dispo)
    db.commit()
    return True