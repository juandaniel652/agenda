from app.db.session import SessionLocal
from app.models.tecnico import Tecnico
from app.schemas.tecnico import TecnicoCreate, TecnicoUpdate
from uuid import UUID
from sqlalchemy import text


MAP_DIAS = {
    "lunes": 0,
    "martes": 1,
    "miercoles": 2,
    "miércoles": 2,
    "jueves": 3,
    "viernes": 4,
    "sabado": 5,
    "sábado": 5,
    "domingo": 6
}


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
    
            # actualizar campos simples
            for key, value in data.dict(exclude_unset=True, exclude={"horarios"}).items():
                setattr(tecnico, key, value)
    
            # si vienen horarios → los actualizo
            if data.horarios is not None:
                db.execute(
                    text("delete from tecnico_disponibilidad where tecnico_id=:id"),
                    {"id": str(id)}
                )
    
                for h in data.horarios:
                    db.execute(
                        text("""
                        insert into tecnico_disponibilidad
                        (tecnico_id, dia_semana, hora_inicio, hora_fin)
                        values (:id, :dia, :inicio, :fin)
                        """),
                        {
                            "id": str(id),
                            "dia": h.dia_semana,
                            "inicio": h.hora_inicio,
                            "fin": h.hora_fin
                        }
                    )
    
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
