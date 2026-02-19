from app.db.session import SessionLocal
from app.models.tecnico import Tecnico
from app.models.tecnico_disponibilidad import TecnicoDisponibilidad
from app.schemas.tecnico import TecnicoCreate, TecnicoUpdate
from uuid import UUID
from sqlalchemy import text
from sqlalchemy.orm import joinedload


class TecnicoService:
    
    @staticmethod
    def crear_tecnico(data: dict):
    
        db = SessionLocal()
    
        try:
        
            tecnico = Tecnico(**data)
    
            db.add(tecnico)
            db.commit()
            db.refresh(tecnico)
    
            return tecnico
    
        finally:
            db.close()


    @staticmethod
    def listar():
        db = SessionLocal()
        try:
            return db.query(Tecnico)\
                     .options(joinedload(Tecnico.horarios))\
                     .filter(Tecnico.activo == True)\
                     .all()
        finally:
            db.close()

    @staticmethod
    def actualizar(id: str, data: TecnicoUpdate):
        db = SessionLocal()
        try:
            tecnico = db.query(Tecnico).filter(Tecnico.id == id).first()

            for field, value in data.dict(exclude={"horarios"}, exclude_unset=True).items():
                setattr(tecnico, field, value)

            if data.horarios is not None:
                db.query(TecnicoDisponibilidad)\
                  .filter(TecnicoDisponibilidad.tecnico_id == id)\
                  .delete()

                for h in data.horarios:
                    nuevo = TecnicoDisponibilidad(
                        tecnico_id=id,
                        dia_semana=h.dia_semana,
                        hora_inicio=h.hora_inicio,
                        hora_fin=h.hora_fin
                    )
                    db.add(nuevo)

            db.commit()
            return tecnico
        finally:
            db.close()



    @staticmethod
    def eliminar(id: UUID):
        db = SessionLocal()
        try:
            tecnico = db.query(Tecnico).get(id)
            if not tecnico:
                raise ValueError("Técnico no encontrado")

            tecnico.activo = False  # soft delete
            db.commit()
            return {"message": "Técnico desactivado"}
        finally:
            db.close()
    