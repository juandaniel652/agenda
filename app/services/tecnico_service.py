from app.db.session import SessionLocal
from app.models.tecnico import Tecnico
from app.schemas.tecnico import TecnicoCreate, TecnicoUpdate
from uuid import UUID

class TecnicoService:

    @staticmethod
    def crear_tecnico(data: TecnicoCreate):
        db = SessionLocal()
        try:
            tecnico = Tecnico(**data.dict())
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
            return db.query(Tecnico).filter(Tecnico.activo == True).all()
        finally:
            db.close()

    @staticmethod
    def actualizar(id: UUID, data: TecnicoUpdate):
        db = SessionLocal()
        try:
            tecnico = db.query(Tecnico).get(id)
            if not tecnico:
                raise ValueError("Técnico no encontrado")

            for key, value in data.dict(exclude_unset=True).items():
                setattr(tecnico, key, value)

            db.commit()
            db.refresh(tecnico)
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
