# app/services/tecnico_service.py
from app.db.session import SessionLocal
from app.models.tecnico import Tecnico
from app.models.tecnico_disponibilidad import TecnicoDisponibilidad
from app.schemas.tecnico import TecnicoCreate, TecnicoUpdate
from sqlalchemy.orm import joinedload
from uuid import UUID


class TecnicoService:

    @staticmethod
    def crear_tecnico(data: dict):
        """Crear un técnico junto con sus horarios opcionales."""
        db = SessionLocal()
        try:
            # Separar horarios del dict antes de crear el modelo
            horarios_data = data.pop("horarios", None)

            tecnico = Tecnico(**data)
            db.add(tecnico)
            db.flush()   # genera el id sin hacer commit aún

            if horarios_data:
                for h in horarios_data:
                    nuevo = TecnicoDisponibilidad(
                        tecnico_id=str(tecnico.id),
                        dia_semana=h["dia_semana"],
                        hora_inicio=h["hora_inicio"],
                        hora_fin=h["hora_fin"]
                    )
                    db.add(nuevo)

            db.commit()
            db.refresh(tecnico)
            return tecnico
        finally:
            db.close()

    @staticmethod
    def listar():
        """Listar todos los técnicos activos con sus horarios."""
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
        """Actualizar un técnico y reemplazar sus horarios si vienen en el payload."""
        db = SessionLocal()
        try:
            tecnico = db.query(Tecnico).filter(Tecnico.id == id).first()
            if not tecnico:
                raise ValueError("Técnico no encontrado")

            # Actualizar campos básicos
            for field, value in data.dict(exclude={"horarios"}, exclude_unset=True).items():
                setattr(tecnico, field, value)

            # Reemplazar horarios si vienen
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
            db.refresh(tecnico)
            return tecnico
        finally:
            db.close()

    @staticmethod
    def eliminar(id: UUID):
        """Soft delete de técnico."""
        db = SessionLocal()
        try:
            tecnico = db.query(Tecnico).get(id)
            if not tecnico:
                raise ValueError("Técnico no encontrado")
            tecnico.activo = False
            db.commit()
            return {"message": "Técnico desactivado"}
        finally:
            db.close()