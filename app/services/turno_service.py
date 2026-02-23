from sqlalchemy.orm import Session
from sqlalchemy import and_
from sqlalchemy.orm import Session, joinedload
from app.models.turno import Turno
from app.schemas.turno import TurnoCreate
from datetime import datetime, timezone


class TurnoService:

    @staticmethod
    def obtener_todos(db: Session):
    
        turnos = db.query(Turno).options(
        
            joinedload(Turno.cliente),
            joinedload(Turno.tecnico)
    
        ).all()
    
        return turnos


    @staticmethod
    def crear(db: Session, turno_data: TurnoCreate):

        conflicto = db.query(Turno).filter(

            Turno.tecnico_id == turno_data.tecnico_id,

            Turno.fecha == turno_data.fecha,

            Turno.estado != "cancelado",

            Turno.hora_inicio < turno_data.hora_fin,

            Turno.hora_fin > turno_data.hora_inicio

        ).first()

        if conflicto:

            raise Exception(
                "El técnico ya tiene un turno en ese horario"
            )

        turno = Turno(**turno_data.dict())

        db.add(turno)

        db.commit()

        db.refresh(turno)

        return turno



    @staticmethod
    def eliminar(db: Session, turno_id):
    
        turno = db.query(Turno).filter(
            Turno.id == turno_id
        ).first()
    
        if not turno:
            raise Exception("Turno no encontrado")
    
        turno.estado = "cancelado"
        turno.cancelado_en = datetime.now(timezone.utc)
    
        db.commit()
        db.refresh(turno)
    
        return turno