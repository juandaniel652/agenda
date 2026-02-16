from sqlalchemy import Column, SmallInteger, Time, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from app.db.base import Base
import uuid

class TecnicoDisponibilidad(Base):
    __tablename__ = "tecnicos_disponibilidad"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tecnico_id = Column(UUID(as_uuid=True), ForeignKey("tecnicos.id"), nullable=False)
    dia_semana = Column(SmallInteger, nullable=False)
    hora_inicio = Column(Time, nullable=False)
    hora_fin = Column(Time, nullable=False)
